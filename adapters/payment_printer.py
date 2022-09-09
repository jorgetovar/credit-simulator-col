from service_layer.money import format_cop


class PaymentWriter:
    def __init__(self, file_name):
        f = open(f'{file_name}.txt', "w+")
        self.file = f

    def write_line(self, line):
        self.file.write(f'{line} \n')
        print(f'{line}')

    def close(self):
        self.file.close()

    def write_time(self, result, state, reduced_years):
        self.write_line(f'total in months: {result.total_months}')
        self.write_line(f'total in years: {result.total_months / 12}')
        self.write_line(f'inflexion point: {result.inflexion_point}')
        self.write_line(f'finish date: {state.due_date}')
        self.write_line(f'total years reduced: {reduced_years}')

    def write_overview(self, result, monthly_principal):
        self.write_line(f'total paid interest: {format_cop(result.total_interest)}')
        self.write_line(f'total paid fee insurances:{format_cop(result.total_fee_insurance)}')
        self.write_line(f'monthly principal: {format_cop(monthly_principal)}')
        self.write_line(f'total paid: {format_cop(result.total_paid)}')
        self.write_line(f'total principal: {format_cop(result.total_principal)}')

    def write_loan(self, property_price, total_due, interest_rate_per_year, interest_rate_per_month, installments,
                   fee_life_insurance, fee_disaster_insurance, initial_payment):
        self.write_line(f'property price: {format_cop(property_price)}')
        self.write_line(f'total due: {format_cop(total_due)}')
        self.write_line(f'interest rate per year: {interest_rate_per_year} %')
        self.write_line(f'interest rate per month: {interest_rate_per_month} %')
        self.write_line(f'installments: {installments}')
        self.write_line(f'fee life insurance: {format_cop(fee_life_insurance)}')
        self.write_line(f'fee disaster insurance: {format_cop(fee_disaster_insurance)}')
        self.write_line(f'initial payment: {format_cop(initial_payment)}')

    def write_due_information(self, fee_insurance, month_due, month_fee_life_insurance, month_interest_due, month_paid,
                              month_principal_due, new_total_due, principal_fixed_payment, principal_payment):
        self.write_line(f'principal fixed payment: {format_cop(principal_fixed_payment)}')
        self.write_line(f'principal payment: {format_cop(principal_payment)}')
        self.write_line(f'interest due: {format_cop(month_interest_due)}')
        self.write_line(f'due: {format_cop(month_due)}')
        self.write_line(f'principal due: {format_cop(month_principal_due)}')
        self.write_line(f'fees life insurance: {format_cop(month_fee_life_insurance)}')
        self.write_line(f'fees insurance due: {format_cop(fee_insurance)}')
        self.write_line(f'total due: {format_cop(new_total_due)} \n')
        self.write_line(f'month paid: {format_cop(month_paid)} \n')
