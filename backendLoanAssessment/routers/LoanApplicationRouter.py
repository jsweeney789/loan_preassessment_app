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

def getLoanService(sagemaker_service: SageMakerService = Depends(getSageMakerService), 
                   db: Session = Depends(get_db)):
    return LoanApplicationService(sagemaker_service, db)

@router.post("/application",  status_code=201)
def submitApplication(
    application: LoanApplication,
    service: LoanApplicationService = Depends(getLoanService),
    user = Depends(getCurrentUser)
) -> ApplicationResult:
    result = service.processApplication(application, user)
    return result

@router.get("/my-applications", status_code=200)
def getUserApplications(
    user = Depends(getCurrentUser),
    service: LoanApplicationService = Depends(getLoanService)
):
    result = service.getUserApplications(user)
    return result