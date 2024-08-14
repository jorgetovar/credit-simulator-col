from dateutil.relativedelta import relativedelta

from adapters.payment_printer import PaymentWriter
from domain.model import State, Due, PaymentPlan
from service_layer.money import format_cop


def generate(loan, first_due_date, file_name):
    result = PaymentPlan()

    writer = PaymentWriter(file_name)
    state = State(False, first_due_date)

    property_price = loan.property_price
    total_due = loan.total_due
    interest_rate_per_year = loan.interest_rate_per_year
    installments = loan.installments
    fee_life_insurance = loan.fee_life_insurance
    fee_disaster_insurance = loan.fee_disaster_insurance
    monthly_principal = loan.monthly_principal
    principal_dict = loan.principal_dict
    interest_rate_per_month = pow(1 + interest_rate_per_year, (30 / 360)) - 1
    initial_payment = property_price - total_due

    def get_month_rate_installment():
        return pow(1 + interest_rate_per_month, installments)

    def get_month_due(actual_amount_due):
        return total_due * (
                (interest_rate_per_month * get_month_rate_installment()) / (get_month_rate_installment() - 1)) \
            + get_fee_insurance_cost(actual_amount_due)

    def get_month_interest_due(actual_amount_due):
        return actual_amount_due * interest_rate_per_month

    def get_fee_life_insurance_cost(actual_amount_due):
        return actual_amount_due * fee_life_insurance / total_due

    def get_fee_insurance_cost(actual_amount_due):
        return fee_disaster_insurance + get_fee_life_insurance_cost(actual_amount_due)

    def get_due(actual_amount_due, principal_payment=0):
        writer.write_line(f'----- month plan {result.total_months} [{state.due_date}] ------')
        principal_fixed_payment = principal_payment
        if state.due_date.isoformat() in principal_dict:
            extraordinary_payment = principal_dict[state.due_date.isoformat()]
            writer.write_line(f'principal extraordinary payment: {format_cop(extraordinary_payment)}')
            principal_payment = principal_payment + extraordinary_payment

        state.due_date = state.due_date + relativedelta(months=+1)

        if result.total_months in principal_dict:
            extraordinary_payment = principal_dict[result.total_months]
            writer.write_line(f'principal extraordinary payment: {format_cop(extraordinary_payment)}')
            principal_payment = principal_payment + extraordinary_payment

        month_due = get_month_due(actual_amount_due)
        if result.month_due is None:
            result.month_due = month_due
        month_interest_due = get_month_interest_due(actual_amount_due)
        fee_insurance = get_fee_insurance_cost(actual_amount_due)
        month_principal_due = month_due - month_interest_due - fee_insurance
        new_total_due = actual_amount_due - month_principal_due - principal_payment
        month_fee_life_insurance = get_fee_life_insurance_cost(actual_amount_due)

        if month_principal_due > month_interest_due and not state.inflexion_point_detected:
            result.inflexion_point = result.total_months
            state.inflexion_point_detected = True
        result.total_principal = result.total_principal + principal_payment
        month_paid = month_due + principal_payment
        result.total_paid = result.total_paid + month_paid

        writer.write_due_information(fee_insurance, month_due, month_fee_life_insurance, month_interest_due, month_paid,
                                     month_principal_due, new_total_due, principal_fixed_payment, principal_payment)

        return Due(month_interest_due, month_due, month_principal_due, month_fee_life_insurance, new_total_due,
                   fee_insurance)

    def payment_plan_fixed_terms(actual_amount_due, to_principal=0):

        if actual_amount_due > 0:
            writer.write_line(f'----- current balance {format_cop(actual_amount_due)} ----- ')
            result.total_months = result.total_months + 1
            plan = get_due(actual_amount_due, to_principal)
            result.total_fee_insurance = result.total_fee_insurance + plan.insurance
            result.total_interest = result.total_interest + plan.month_payment_interest
            actual_amount_due = payment_plan_fixed_terms(plan.balance, to_principal)
        else:
            reduced_years = installments / 12 - result.total_months / 12
            reduced_years = 0 if reduced_years < 0 else reduced_years
            result.interest_rate_per_month = interest_rate_per_month
            result.total_in_years = result.total_months / 12
            result.reduced_years = reduced_years

            writer.write_line('*************************')
            writer.write_line('------ Overview ------')
            writer.write_overview(result, monthly_principal)
            writer.write_line('------ loan ------')
            writer.write_loan(property_price, total_due, interest_rate_per_year, interest_rate_per_month, installments,
                              fee_life_insurance, fee_disaster_insurance, initial_payment)
            writer.write_line('------ time ------')
            writer.write_time(result, state, reduced_years)
            writer.write_line('*************************')

        return actual_amount_due

    writer.write_line(f'----- PAYMENT-PLAN -----\n')
    payment_plan_fixed_terms(total_due, monthly_principal)
    writer.close()
    return result
