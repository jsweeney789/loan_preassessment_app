from fastapi import APIRouter, Depends
from backendLoanAssessment.security.dependencies import getCurrentUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(user=Depends(getCurrentUser)):
    return user

'''
Some security notes here:

SpringBoot architecture has a lovely security context system that we get to work within, FastAPI just reuses dependency injection.

For an endpoint that relies on security, we would include user=Depends(getCurrentUser) just like this one, which calls the getCurrentUser and authenticates
it for us. We can also do this a the touer level.
'''