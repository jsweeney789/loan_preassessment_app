from backendLoanAssessment.schemas.LoanApplication import *
from backendLoanAssessment.services import SageMakerService
from backendLoanAssessment.constants.AdviceStrings import *
from copy import deepcopy

BIG_RISK_THRESHOLD = 0.3
RISK_THRESHOLD = 0.15
BIG_SAFE_THRESHOLD = -0.3
SAFE_THRESHOLD = -0.15

SIGNIFICANT_SCORE_DIFF = 0.1

class AdviceService:
    def __init__(self, sagemakerService: SageMakerService):
        self.sagemaker = sagemakerService

    def computeScoreDiffWithModification(
        self,
        originalLoanApp,
        prediction,
        fieldToModify,
        modificationOperation
    ):

        modifiedLoanApp = deepcopy(originalLoanApp)

        currentValue = getattr(modifiedLoanApp, fieldToModify)
        newValue = modificationOperation(currentValue)
        setattr(modifiedLoanApp, fieldToModify, newValue)

        newPrediction, _ = self.sagemaker.predictWithExplanations(modifiedLoanApp)

        scoreDiff = calculateScoreDiff(prediction, newPrediction)

        return scoreDiff

    def generateUserAdvice(self, mlApplication, prediction, explanations):
        userAdvice = {"GOOD": [], "BAD": [], "INFO": []}

        '''
        AGE
        '''
        ageScore = explanations["Age"]
        match ageScore:
            case x if x >= RISK_THRESHOLD:
                appendAdvice(userAdvice, "INFO", ageScore, AGE_RISK.format(age=mlApplication.age))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", ageScore, AGE_SAFE.format(age=mlApplication.age))

        '''
        JOB
        '''
        jobScore = explanations["Job"]
        match jobScore:
            case x if x >= RISK_THRESHOLD:
                scoreDiff = 0

                if mlApplication.job < 3:
                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='job',
                        modificationOperation=lambda x: x + 1
                    )
                
                if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                    appendAdvice(userAdvice, "BAD", jobScore,
                            JOB_RISK_POINTS.format(
                                jobPlus1=employmentStringMap[mlApplication.job + 1],
                                diff=scoreDiff,
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", jobScore, JOB_RISK.format(job=employmentStringMap[mlApplication.job]))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", jobScore, JOB_BIG_SAFE.format(job=employmentStringMap[mlApplication.job]))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", jobScore, JOB_SAFE.format(job=employmentStringMap[mlApplication.job]))

        '''
        HOUSING
        '''

        '''
        SAVING ACCOUNTS
        '''

        '''
        CHECKING ACCOUNTS
        '''

        '''
        CREDIT AMOUNT
        '''
        
        '''
        DURATION
        '''

        '''
        SEX
        '''

        '''
        PURPOSE
        '''
        return userAdvice


def calculateScoreDiff(prediction, newPrediction):
    return round((prediction - newPrediction) * 100, 1)


def appendAdvice(userAdvice, adviceType, score, displayStr):
    userAdvice[adviceType].append((score, displayStr))

