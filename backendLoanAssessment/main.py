from fastapi import FastAPI
from backendLoanAssessment.routers import loan_applications

app = FastAPI(title="Loan Risk Portal")

app.include_router(loan_applications.router, prefix="/applications", tags=["Applications"])