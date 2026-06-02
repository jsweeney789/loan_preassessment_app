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
                            RISK_POINTS.format(
                                field='employment',
                                plus1=employmentStringMap[mlApplication.job + 1],
                                diff=scoreDiff,
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", jobScore, RISK.format(field='employment', current=employmentStringMap[mlApplication.job]))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", jobScore, BIG_SAFE.format(field='employment', current=employmentStringMap[mlApplication.job]))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", jobScore, SAFE.format(field='employment', current=employmentStringMap[mlApplication.job]))

        '''
        HOUSING
        '''
        housingScore = explanations["Housing"]
        match housingScore:
            case x if x >= RISK_THRESHOLD:
                scoreDiff = 0

                if mlApplication.housing < 2:
                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='housing',
                        modificationOperation=lambda x: x + 1
                    )
                
                if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                    appendAdvice(userAdvice, "BAD", housingScore,
                            RISK_POINTS.format(
                                field='housing',
                                plus1=homeOwnershipStringMap[mlApplication.housing + 1],
                                diff=scoreDiff,
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", housingScore, RISK.format(field='housing',current=homeOwnershipStringMap[mlApplication.housing]))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", housingScore, BIG_SAFE.format(field='housing',current=homeOwnershipStringMap[mlApplication.housing]))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", housingScore, SAFE.format(field='housing',current=homeOwnershipStringMap[mlApplication.housing]))
        
        '''
        SAVING ACCOUNTS
        '''
        savingScore = explanations["Saving accounts"]
        match savingScore:
            case x if x >= RISK_THRESHOLD:
                scoreDiff = 0

                if mlApplication.savingAcc < 4:
                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='savingAcc',
                        modificationOperation=lambda x: x + 1
                    )
                
                if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                    appendAdvice(userAdvice, "BAD", savingScore,
                            ACCOUNT_RISK_POINTS.format(
                                field='savings account',
                                plus1=savingAccStringMap[mlApplication.savingAcc + 1],
                                diff=scoreDiff,
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", savingScore, ACCOUNT_RISK.format(field='savings account'))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", savingScore, ACCOUNT_BIG_SAFE.format(field='savings account'))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", savingScore, ACCOUNT_SAFE.format(field='savings account'))

        '''
        CHECKING ACCOUNTS
        '''
        checkingScore = explanations["Checking account"]
        match checkingScore:
            case x if x >= RISK_THRESHOLD:
                scoreDiff = 0
                plusOne = 4
                checkingAccVal = mlApplication.checkingAcc

                if checkingAccVal < 4:
                    if checkingAccVal != 2:
                        plusOne = checkingAccVal + 1
                    # Else plusOne  = 4
                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='checkingAcc',
                        modificationOperation = lambda x: plusOne
                    )
                
                if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                    appendAdvice(userAdvice, "BAD", checkingScore,
                            ACCOUNT_RISK_POINTS.format(
                                field='checking account',
                                plus1=checkingAccStringMap[plusOne],
                                diff=scoreDiff,
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", checkingScore, ACCOUNT_RISK.format(field='checking account'))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", checkingScore, ACCOUNT_BIG_SAFE.format(field='checking account'))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", checkingScore, ACCOUNT_SAFE.format(field='checking account'))

        '''
        CREDIT AMOUNT
        '''
        amountScore = explanations["Credit amount"]
        
        match amountScore:
            
            case x if x >= RISK_THRESHOLD:
                    scoreDiff = 0 
                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='creditAmount',
                        modificationOperation = lambda x: x * 0.9
                    )
                
                    if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                        # TODO: Convert back to USD to display to the user
                        roundedAmount = round(mlApplication.creditAmount * 0.9)
                        formattedAmount = "{:,}".format(roundedAmount)
                        appendAdvice(userAdvice, "BAD", amountScore,
                                LOAN_RISK_POINTS.format(
                                    tenOff=formattedAmount, 
                                    diff=scoreDiff,
                                ))
                    
                    else:
                        appendAdvice(userAdvice, "BAD", amountScore, LOAN_RISK)

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", amountScore, LOAN_BIG_SAFE)
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", amountScore, LOAN_SAFE)

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

