from fastapi import APIRouter, Depends
from backendLoanAssessment.security.dependencies import getCurrentUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user=Depends(getCurrentUser)):
    return user

