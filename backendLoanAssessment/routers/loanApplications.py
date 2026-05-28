from fastapi import APIRouter, Depends
from backendLoanAssessment.schemas.LoanApplication import LoanApplication
from backendLoanAssessment.services import LoanApplicationService


router = APIRouter()

def getLoanService():
    return LoanApplicationService()

@router.post("/",  status_code=201)
def submit_application(
    application: LoanApplication,
    service: LoanApplicationService = Depends(getLoanService)
):
    result = service.processApplication(application)
    return result