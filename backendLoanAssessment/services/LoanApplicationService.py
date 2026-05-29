from backendLoanAssessment.schemas.LoanApplication import *
from backendLoanAssessment.services import SageMakerService, UserAdviceHelper

class LoanApplicationService:
    def __init__(self, sagemakerService: SageMakerService):
        self.sagemaker = sagemakerService

    def processApplication(self, application: LoanApplication) -> ApplicationResult:
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

        # Credit amount needs to be converted to numeric ints, may also need to be contextualized for modern USD
        mlCreditAmount = application.creditAmount

        # Duration - is already numeric in months, can be untouched
        mlDuration = application.duration

        # Purpose - make sure it's mapped exactly to the categorical strings in the ML
        mlPurpose = LoanPurpose.encodePurpose(application.purpose)


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

        userAdvice = UserAdviceHelper.generateUserAdvice(mlApplication, prediction, explanations)

        result = ApplicationResult(
            decision = self.processPrediction(prediction),
            prediction = prediction,
            userAdvice = userAdvice,
            explanations = explanations
        )
        print(result)

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