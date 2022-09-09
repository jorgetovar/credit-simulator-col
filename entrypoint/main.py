import datetime

from service_layer import payment_plan_service
from domain.model import Loan

loan = Loan(property_price=441_000_000,
            total_due=300_000_000,
            interest_rate_per_year=0.103999,
            installments=120,
            fee_life_insurance=210_000,
            fee_disaster_insurance=114_000)

if __name__ == '__main__':
    first_due_date = datetime.date(2020, 10, 28)
    payment_plan_service.generate(loan, first_due_date, 'production_payment_plan')
