import os
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from backendLoanAssessment.database import get_db
from backendLoanAssessment.services.AuthService import loginOrCreateUser
from backendLoanAssessment.services.GoogleOauthService import oauth
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login(request: Request):
    """Redirect the user to Google's OAuth consent screen."""
    redirect_uri = request.url_for("authCallback")
    return await oauth.google.authorize_redirect(request, redirect_uri)



@router.get("/callback", name="authCallback")
async def authCallback(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Google redirects here after the user authenticates.
    Exchange the code for a token, fetch the user info,
    then log in or create the user and return a JWT.
    """
    google_token = await oauth.google.authorize_access_token(request)
    google_user = google_token.get("userinfo")

    if not google_user:
        google_user = await oauth.google.userinfo(token=google_token)

    jwt_token, user = loginOrCreateUser(db, google_user)

    # TODO
    response = RedirectResponse(url=os.getenv("FRONTEND_URL", "http://localhost:4200/loanapplication"))
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,      # JS cannot read it
        secure=os.getenv("ENVIRONMENT") != "development",        # HTTP or HTTP depending on local dev, worth testing if this actually works
        samesite="lax",     # sent on normal navigation, blocked on cross-site POST
        max_age=3600        # matches your 1 hour token expiry
    )

    return response
    