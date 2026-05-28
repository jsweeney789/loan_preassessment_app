from schemas import LoanApplication
class LoanApplicationService:

    def processApplication(self, application: LoanApplication):
        # Example logic
        if application.credit_score < 600:
            return {
                "status": "rejected",
                "reason": "Credit score too low"
            }

        if application.amount > application.income * 5:
            return {
                "status": "rejected",
                "reason": "Debt-to-income too high"
            }

        # Pretend we save to DB or trigger workflow here
        return {
            "status": "approved",
            "approved_amount": application.amount
        }