from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Cookie
from backendLoanAssessment.database import get_db
from backendLoanAssessment.security.jwt import decodeJwtToken
from backendLoanAssessment.models.UserModel import UserModel as User

'''
More FastAPI Security notes:

This is the "SecurityFilterChain" in FastAPI. 
Functions or routers can depends on this method which requires us to have and decode a valid JWT token

'''
def getCurrentUser(
    access_token: str = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decodeJwtToken(access_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user