import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backendLoanAssessment.routers.LoanApplicationRouter import router as loan_router
from backendLoanAssessment.database import Base, engine
from backendLoanAssessment.models.UserModel import UserModel
from backendLoanAssessment.models.LoanApplicationModel import LoanApplicationModel
from backendLoanAssessment.models.ApplicationResultModel import ApplicationResultModel
from backendLoanAssessment.routers.AuthRouter import router as auth_router
from backendLoanAssessment.routers.UserRouter import router as user_router
from starlette.middleware.sessions import SessionMiddleware



# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Risk Portal")

_cors_origins = os.getenv("CORS_ORIGIN", "http://localhost:4200,https://d1u5g6nu2nj7p1.cloudfront.net").split(",")

# apparently this is used when authlib generaetes a state value and wants a place to store it while oauth does some stuff

is_production = os.getenv("ENVIRONMENT") != "development"

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET"),
    https_only=is_production,
    same_site="none" if is_production else "lax",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)



app.include_router(loan_router, prefix="/api", tags=["Applications"])
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}