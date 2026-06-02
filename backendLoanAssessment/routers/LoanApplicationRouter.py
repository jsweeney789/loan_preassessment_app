from fastapi import APIRouter, Depends
from backendLoanAssessment.schemas import LoanApplication, ApplicationResult
from backendLoanAssessment.services.LoanApplicationService import LoanApplicationService
from backendLoanAssessment.services import SageMakerService
from backendLoanAssessment.security.dependencies import getCurrentUser
from sqlalchemy.orm import Session
from backendLoanAssessment.database import get_db

router = APIRouter(prefix="/loans", tags=["loans"])

def getSageMakerService():
    return SageMakerService()

def getLoanService(sagemaker_service: SageMakerService = Depends(getSageMakerService)):
    return LoanApplicationService(sagemaker_service)

@router.post("/application",  status_code=201)
def submitApplication(
    application: LoanApplication,
    service: LoanApplicationService = Depends(getLoanService),
    db: Session = Depends(get_db)
) -> ApplicationResult:
    result = service.processApplication(application)
    return result

@router.get("/my-applications", status_code=200)
def getUserApplications(
    user = Depends(getCurrentUser),
    service: LoanApplicationService = Depends(getLoanService),
    db: Session = Depends(get_db)
):
    result = service.getUserApplications(user)
    return result