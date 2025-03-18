import datetime
from typing import Optional, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.domain.model import Loan
from app.service_layer import payment_plan_service
from app.service_layer.money import format_cop

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization", "accept", "Origin", "Access-Control-Request-Method", "Access-Control-Request-Headers"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


class PaymentPlanResponse(BaseModel):
    total_interest: float
    total_months: int
    total_fee_insurance: float
    inflexion_point: int
    interest_rate_per_month: float
    total_paid: float
    total_paid_plus_initial_payment: float
    total_in_years: float
    reduced_years: float
    month_due: float
    total_principal: float
    # Add the file field to the response model array of strings
    file: List[str]

    def format_fields(self):
        return {
            "total_interest": format_cop(self.total_interest),
            "total_months": self.total_months,
            "total_fee_insurance": format_cop(self.total_fee_insurance),
            "inflexion_point_in_months": f"{self.inflexion_point} months where 20% of the payment is interest",
            "interest_rate_per_month": f"{self.interest_rate_per_month:.3%}",
            "total_paid": format_cop(self.total_paid),
            "total_paid_plus_initial_payment": format_cop(self.total_paid_plus_initial_payment),
            "total_in_years": self.total_in_years,
            "reduced_years": self.reduced_years,
            "month_due": format_cop(self.month_due),
            "total_principal": format_cop(self.total_principal),
            "payment_plan": self.file
        }


class LoanModel(BaseModel):
    property_price: float
    total_due: float
    interest_rate_per_year: float
    installments: int
    fee_life_insurance: float
    fee_disaster_insurance: float
    monthly_principal: Optional[float] = 0
    principal_dict: Optional[Dict[str, float]] = {}

    class Config:
        orm_mode = True


@app.get("/")
def hello_aws_community_builders():
    return {"Hello": "AWS Community Builders!"}


@app.post("/credit/simulate")
async def simulate_credit(loan: LoanModel, first_due_date: str):
    try:
        first_due_date = datetime.datetime.strptime(first_due_date, "%Y-%m-%d")

        loan_obj = Loan(
            property_price=loan.property_price,
            total_due=loan.total_due,
            interest_rate_per_year=loan.interest_rate_per_year,
            installments=loan.installments,
            fee_life_insurance=loan.fee_life_insurance,
            fee_disaster_insurance=loan.fee_disaster_insurance,
            monthly_principal=loan.monthly_principal,
            principal_dict=loan.principal_dict,
        )

        payment_plan, file = payment_plan_service.generate(loan_obj, first_due_date, 'production_payment_plan')
        response_model = PaymentPlanResponse(
            total_interest=payment_plan.total_interest,
            total_months=payment_plan.total_months,
            total_fee_insurance=payment_plan.total_fee_insurance,
            inflexion_point=payment_plan.inflexion_point,
            interest_rate_per_month=payment_plan.interest_rate_per_month,
            total_paid=payment_plan.total_paid,
            total_paid_plus_initial_payment=payment_plan.total_paid + (loan.property_price - loan.total_due),
            total_in_years=payment_plan.total_in_years,
            reduced_years=payment_plan.reduced_years,
            month_due=payment_plan.month_due,
            total_principal=payment_plan.total_principal,
            file=file
        )

        return response_model.format_fields()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
