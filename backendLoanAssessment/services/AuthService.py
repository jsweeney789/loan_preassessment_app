from sqlalchemy.orm import Session
from backendLoanAssessment.models.UserModel import UserModel as User
from backendLoanAssessment.security.jwt import createJwtToken


# For oauth these are kind of the same thing
def loginOrCreateUser(db: Session, google_user: dict):
    user = db.query(User).filter(
        User.google_sub == google_user["sub"]
    ).first()

    if not user:
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