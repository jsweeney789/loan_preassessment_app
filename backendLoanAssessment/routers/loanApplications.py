from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backendLoanAssessment.schemas.LoanApplication import LoanApplication
from backendLoanAssessment.services import LoanApplicationService


router = APIRouter()

@router.post("/",  status_code=201)
def submit_application(

):
    return None