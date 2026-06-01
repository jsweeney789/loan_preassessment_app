import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backendLoanAssessment.routers.LoanApplicationRouter import router
from backendLoanAssessment.database import Base, engine
from backendLoanAssessment import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loan Risk Portal")

_cors_origins = os.getenv("CORS_ORIGIN", "http://localhost:4200", "https://d1u5g6nu2nj7p1.cloudfront.net").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["Applications"])

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}