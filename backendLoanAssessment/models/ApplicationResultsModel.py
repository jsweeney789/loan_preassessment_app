from sqlalchemy import Column, Integer, Float, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from backendLoanAssessment.database import Base

class ApplicationResultModel(Base):
    __tablename__ = "application_results"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"), nullable=False)

    prediction = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    user_advice = Column(JSON, nullable=False)
    explanations = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("LoanApplicationModel", back_populates="result")