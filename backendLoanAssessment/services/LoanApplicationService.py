from backendLoanAssessment.schemas.LoanApplicationSchema import *
from backendLoanAssessment.services.AdviceService import AdviceService
from backendLoanAssessment.services.SageMakerService import SageMakerService
from backendLoanAssessment.models import ApplicationResultModel, UserModel as User, LoanApplicationModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

class LoanApplicationService:
    def __init__(self, sagemakerService: SageMakerService, db: Session):
        self.sagemaker = sagemakerService
        self.advice_service = AdviceService(sagemakerService)
        self.db = db

    def processApplication(self, application: LoanApplication, user: User) -> ApplicationResult:
        print("At start of processApplication in service")
        # Save the human readable LoanApplication to our db
        dbApplication = self.saveLoanAppToDB(application, user)
        print("Saved loan to db")
        # the general purpose of this service is to process each LoanApplication from our frontend into something the ML can predict on
        print(application)
        # age can be untouched
        mlAge = application.age

        # sex can be untouched I think, might have to convert to numerical
        mlSex = sexNumericMap[application.sex]

        # Job needs to be mapped to 0,1,2,3
        mlJob = employmentNumericMap[application.job]

        # Housing should be mapped to 0,1,2 for free, rent, own respectively
        mlHousing = homeOwnershipNumericMap[application.housing]

        # Checking Accounts need to be mapped to NA, little, moderate, quite rich, rich but expect less than savings and also map to 2026 USD if possible
        mlChecking = CheckingAccountStatus.classify(application.checkingAcc).value


        # Savings Accounts need to be mapped to the same values as above essentially
        mlSavings = SavingsAccountStatus.classify(application.savingAcc).value

        # Credit amount needs to be converted to numeric ints, may also need to be contextualized from modern USD -> 1974 DM
        usd1974Credit = application.creditAmount / 6.57 # found using https://aier.org/cost-of-living-calculator/?utm_source=Google%20Ads&utm_medium=Google%20CPC&utm_campaign=COLA&gad_source=1&gad_campaignid=1488531787&gbraid=0AAAAADn50P7ebwdhCoiMyZNdUwXjFQmro&gclid=CjwKCAjw8uTQBhAdEiwAVvtJyk9YZh5MIeetYo6r5tmVxlTFuN0DnPixiAoGKtSrmJqumcVm4mNflBoC76IQAvD_BwE
        dm1974Credit = 2.758 * usd1974Credit # found here https://marcuse.faculty.history.ucsb.edu/projects/currency.htm
        mlCreditAmount = round(dm1974Credit)

        # Duration - is already numeric in months, can be untouched
        mlDuration = application.duration

        # Purpose - make sure it's mapped exactly to the categorical strings in the ML
        mlPurpose = LoanPurpose.encodePurpose(application.purpose)
        print("Finished ml computations")

        mlApplication = MLLoanApplication(
            age=mlAge,
            job=mlJob,
            housing=mlHousing,
            savingAcc=mlSavings,
            checkingAcc=mlChecking,
            creditAmount=mlCreditAmount,
            duration=mlDuration,
            Sex_male=mlSex,
            **mlPurpose
        )
        print(mlApplication)

        # calling our SageMaker Endpoint
        prediction, explanations = self.sagemaker.predictWithExplanations(mlApplication)
        print(prediction)

        userAdvice = self.advice_service.generateUserAdvice(mlApplication, prediction, explanations)

        result = ApplicationResult(
            decision = self.processPrediction(prediction),
            prediction = prediction,
            userAdvice = userAdvice,
            explanations = explanations
        )
        print(result)

        # Save the result to our db as well
        self.saveAppResultsToDB(result, dbApplication.id)

        return result
    
    def processPrediction(self, prediction) -> LoanDecision:
        # some kind of logic to return the prediction as a meaningful value
        # note that 0 is a good credit score and 1 is a poor one
        if prediction < 0.2:
            return LoanDecision.confident_approval
        elif prediction < 0.4:
            return LoanDecision.likely_approval
        elif prediction < 0.6:
            return LoanDecision.unsure
        elif prediction < 0.8:
            return LoanDecision.likely_disapproval
        else:
            return LoanDecision.confident_disapproval
    
    def getUserApplications(self, user):
        return (
            self.db.query(LoanApplicationModel)
            .filter(LoanApplicationModel.user_id == user.id)
            .options(joinedload(LoanApplicationModel.result))
            .all()
        )
    
    def saveLoanAppToDB(self, application: LoanApplication, user: User):
        db_application = LoanApplicationModel(
            user_id=user.id,
            age=application.age,
            sex=application.sex,
            job=application.job,
            housing=application.housing,
            checking_acc=application.checkingAcc,
            saving_acc=application.savingAcc,
            credit_amount=application.creditAmount,
            duration=application.duration,
            purpose=application.purpose
        )
        self.db.add(db_application)
        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def saveAppResultsToDB(self, result: ApplicationResult, dbAppId: int):
        db_result = ApplicationResultModel(
            application_id=dbAppId,
            prediction=result.prediction,
            decision=result.decision,
            user_advice=result.userAdvice,
            explanations=result.explanations
        )
        self.db.add(db_result)
        self.db.commit()

        return db_result