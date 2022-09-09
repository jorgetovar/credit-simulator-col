import datetime
import unittest
from service_layer import payment_plan_service

from domain.model import Loan

expected = {'total_interest': 174443906.52459008,
            'total_months': 120,
            'total_fee_insurance': 28429449.012546323,
            'inflexion_point': 37,
            'interest_rate_per_month': 0.008279003131801188,
            'total_paid': 502873355.53713715,
            'total_in_years': 10.0,
            'reduced_years': 0.0,
            'month_due': 4277699.221038255,
            'total_principal': 0}

loan = Loan(property_price=441_000_000,
            total_due=300_000_000,
            interest_rate_per_year=0.103999,
            installments=120,
            fee_life_insurance=210_000,
            fee_disaster_insurance=114_000)

loan_monthly = Loan(property_price=441_000_000,
                    total_due=300_000_000,
                    interest_rate_per_year=0.103999,
                    installments=120,
                    fee_life_insurance=210_000,
                    fee_disaster_insurance=114_000,
                    monthly_principal=1_000_000)


class TestPayment(unittest.TestCase):
    def test_plan(self):
        first_due_date = datetime.date(2020, 10, 28)
        result = payment_plan_service.generate(loan, first_due_date, 'test_payment_plan')
        self.assertEqual(result.__dict__, expected)

    def test_plan_state(self):
        first_due_date = datetime.date(2020, 10, 28)
        result = payment_plan_service.generate(loan, first_due_date, 'test_payment_plan')
        self.assertEqual(result.__dict__, expected)

    def test_plan_principal(self):
        first_due_date = datetime.date(2020, 10, 28)
        result = payment_plan_service.generate(loan_monthly, first_due_date, 'test_payment_plan')
        expected_principal = {'inflexion_point': 24,
                              'interest_rate_per_month': 0.008279003131801188,
                              'month_due': 4277699.221038255,
                              'reduced_years': 2.916666666666667,
                              'total_fee_insurance': 19677591.388224065,
                              'total_in_years': 7.083333333333333,
                              'total_interest': 118124714.83179663,
                              'total_months': 85,
                              'total_paid': 440742025.1764757,
                              'total_principal': 85000000}
        self.assertEqual(result.__dict__, expected_principal)


if __name__ == '__main__':
    unittest.main()
