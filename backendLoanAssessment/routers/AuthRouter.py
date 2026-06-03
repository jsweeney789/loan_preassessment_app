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
    frontend_url = request.query_params.get("redirect", "http://localhost:4200")
    return await oauth.google.authorize_redirect(request, redirect_uri, state=frontend_url)



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

    frontend_url = request.query_params.get("state", "http://localhost:4200")
    if not is_safe_redirect(frontend_url):
        frontend_url = "http://localhost:4200"

    response = RedirectResponse(url=frontend_url)
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,      # JS cannot read it
        secure=os.getenv("ENVIRONMENT") != "development",        # HTTP or HTTP depending on local dev, worth testing if this actually works
        samesite="lax",     # sent on normal navigation, blocked on cross-site POST
        max_age=3600        # matches your 1 hour token expiry
    )

    return response
    
from urllib.parse import urlparse

ALLOWED_HOSTS = {"localhost", "d1u5g6nu2nj7p1.cloudfront.net"}

def is_safe_redirect(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.hostname in ALLOWED_HOSTS
    except Exception:
        return False

