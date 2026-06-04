from sqlalchemy.orm import Session
from backendLoanAssessment.models.UserModel import UserModel as User
from backendLoanAssessment.security.jwt import createJwtToken
from passlib.context import CryptContext
from fastapi import HTTPException

# For oauth these are kind of the same thing
def loginOrCreateUser(db: Session, google_user: dict):
    user = db.query(User).filter(User.google_sub == google_user["sub"]).first()
    
    if not user:
        # Check if they registered with password using same email
        user = db.query(User).filter(User.email == google_user["email"]).first()
        if user:
            # Link their Google sub to the existing account
            user.google_sub = google_user["sub"]
        else:
            # Brand new user
            user = User(
                google_sub=google_user["sub"],
                email=google_user["email"],
                name=google_user.get("name")
            )
            db.add(user)
            
        db.commit()
        db.refresh(user)

    token = createJwtToken(
        {"sub": str(user.id)}
    )

    return token, user

pwd_context = CryptContext(schemes=["bcrypt"])
def registerUser(db: Session, email: str, password: str):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")
    user = User(email=email, hashed_password=pwd_context.hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return createJwtToken({"sub": str(user.id)})

def loginWithPassword(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.hashed_password:
        raise HTTPException(401, "Invalid credentials")
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return createJwtToken({"sub": str(user.id)})