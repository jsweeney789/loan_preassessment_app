from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Cookie
from backendLoanAssessment.database import get_db
from backendLoanAssessment.security.jwt import decodeJwtToken
from backendLoanAssessment.models.UserModel import UserModel as User
from typing import Optional


def getOptionalUser(
    access_token: str = Cookie(default=None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not access_token:
        return None
    payload = decodeJwtToken(access_token)
    if not payload:
        return None
    user_id = payload.get("sub")
    return db.query(User).filter(User.id == user_id).first()

def getCurrentUser(
    user: Optional[User] = Depends(getOptionalUser)
):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user