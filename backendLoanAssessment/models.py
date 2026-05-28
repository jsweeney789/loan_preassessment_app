from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from backendLoanAssessment.database import Base


class LoanApplicationRecord(Base):
    __tablename__ = "loan_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[str] = mapped_column(String)
    job: Mapped[str] = mapped_column(String)
    housing: Mapped[str] = mapped_column(String)
    checking_acc: Mapped[int] = mapped_column(Integer)
    saving_acc: Mapped[int] = mapped_column(Integer)
    credit_amount: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    purpose: Mapped[str] = mapped_column(String)

    ml_result: Mapped[str | None] = mapped_column(String, nullable=True)
