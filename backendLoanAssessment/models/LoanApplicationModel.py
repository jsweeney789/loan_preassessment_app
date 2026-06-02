from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backendLoanAssessment.database import Base

class LoanApplicationModel(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    age = Column(Integer, nullable=False)
    sex = Column(String, nullable=False)
    job = Column(String, nullable=False)
    housing = Column(String, nullable=False)
    checking_acc = Column(Integer, nullable=False)
    saving_acc = Column(Integer, nullable=False)
    credit_amount = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    purpose = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")
    result = relationship("ApplicationResultModel", back_populates="application", uselist=False)