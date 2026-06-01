from fastapi import APIRouter, Depends
from backendLoanAssessment.schemas import LoanApplication, ApplicationResult
from backendLoanAssessment.services.LoanApplicationService import LoanApplicationService
from backendLoanAssessment.services import SageMakerService


router = APIRouter(prefix="/loans", tags=["loans"])

def getSageMakerService():
    return SageMakerService()

def getLoanService(sagemaker_service: SageMakerService = Depends(getSageMakerService)):
    return LoanApplicationService(sagemaker_service)

@router.post("/application",  status_code=201)
def submit_application(
    application: LoanApplication,
    service: LoanApplicationService = Depends(getLoanService)
) -> ApplicationResult:
    result = service.processApplication(application)
    return result