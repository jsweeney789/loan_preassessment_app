from sqlalchemy.orm import Session
from backendLoanAssessment.models.UserModel import UserModel as User
from backendLoanAssessment.security.jwt import createJwtToken
import bcrypt
from fastapi import HTTPException

# For oauth these are kind of the same thing
def loginOrCreateUser(db: Session, google_user: dict):
    user = db.query(User).filter(User.google_sub == google_user["sub"]).first()
    
    if not user:
        user = db.query(User).filter(User.email == google_user["email"]).first()
        if user:
            user.google_sub = google_user["sub"]
        else:
            user = User(
                google_sub=google_user["sub"],
                email=google_user["email"],
                name=google_user.get("name")
            )
            db.add(user)
            
        db.commit()
        db.refresh(user)

    token = createJwtToken({"sub": str(user.id)})
    return token, user


def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verifyPassword(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def registerUser(db: Session, email: str, password: str):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=email, hashed_password=hashPassword(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return createJwtToken({"sub": str(user.id)})


def loginWithPassword(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.hashed_password:
        raise HTTPException(401, "Invalid credentials")
    if not verifyPassword(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return createJwtToken({"sub": str(user.id)})