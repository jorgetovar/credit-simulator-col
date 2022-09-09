class State:
    def __init__(self, inflexion_point_detected, due_date):
        self.inflexion_point_detected = inflexion_point_detected
        self.due_date = due_date


class Due:
    def __init__(self, month_payment_interest, month_payment, month_capital,
                 life_insurance, balance, insurance):
        self.month_payment_interest = month_payment_interest
        self.month_payment = month_payment
        self.month_capital = month_capital
        self.life_insurance = life_insurance
        self.balance = balance
        self.insurance = insurance


class Loan:
    def __init__(self, property_price, total_due, interest_rate_per_year,
                 installments, fee_life_insurance, fee_disaster_insurance,
                 monthly_principal=0, principal_dict=None):
        if principal_dict is None:
            principal_dict = {}
        self.property_price = property_price
        self.total_due = total_due
        self.interest_rate_per_year = interest_rate_per_year
        self.installments = installments
        self.fee_life_insurance = fee_life_insurance
        self.fee_disaster_insurance = fee_disaster_insurance
        self.monthly_principal = monthly_principal
        self.principal_dict = principal_dict


class PaymentPlan:
    def __init__(self, total_interest=0, total_months=0,
                 total_fee_insurance=0, inflexion_point=0,
                 interest_rate_per_month=0, total_paid=0,
                 total_in_years=0, reduced_years=0, month_due=None,
                 total_principal=0):
        self.total_interest = total_interest
        self.total_months = total_months
        self.total_fee_insurance = total_fee_insurance
        self.inflexion_point = inflexion_point
        self.interest_rate_per_month = interest_rate_per_month
        self.total_paid = total_paid
        self.total_in_years = total_in_years
        self.reduced_years = reduced_years
        self.month_due = month_due
        self.total_principal = total_principal
