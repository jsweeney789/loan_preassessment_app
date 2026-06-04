from backendLoanAssessment.schemas.LoanApplicationSchema import *
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
                appendAdvice(userAdvice, "INFO", ageScore, AGE_SAFE.format(age=mlApplication.age))

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

                    scoreDiff = self.computeScoreDiffWithModification(
                        originalLoanApp=mlApplication,
                        prediction=prediction,
                        fieldToModify='creditAmount',
                        modificationOperation = lambda x: x * 0.9
                    )
                
                    if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                        
                        dmConvertedAmount = mlApplication.creditAmount/0.419786910198 * 0.9
                        formattedAmount = "{:,}".format(int(dmConvertedAmount))
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
        durationScore = explanations["Duration"]
        match durationScore:
            case x if x >= RISK_THRESHOLD:
                shorterScoreDiff = self.computeScoreDiffWithModification(
                    originalLoanApp=mlApplication,
                    prediction=prediction,
                    fieldToModify='duration',
                    modificationOperation = lambda x: round(x / 1.5)
                )
                longerScoreDiff = self.computeScoreDiffWithModification(
                    originalLoanApp=mlApplication,
                    prediction=prediction,
                    fieldToModify='duration',
                    modificationOperation = lambda x: round(x * 1.5)
                )

                if shorterScoreDiff > longerScoreDiff:
                    scoreDiff = shorterScoreDiff
                    adjustedDuration = round(mlApplication.duration / 1.5)
                else:
                    scoreDiff = longerScoreDiff
                    adjustedDuration = round(mlApplication.duration * 1.5)
                
                if scoreDiff >= SIGNIFICANT_SCORE_DIFF:
                    appendAdvice(userAdvice, "BAD", durationScore,
                            DURATION_RISK_POINTS.format(
                                adjusted=str(adjustedDuration) + " months",
                                diff=scoreDiff
                            ))
                   
                else:
                    appendAdvice(userAdvice, "BAD", durationScore, DURATION_RISK.format(current=str(mlApplication.duration) + " months"))

            case x if x <= BIG_SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", durationScore, DURATION_BIG_SAFE.format(current=str(mlApplication.duration) + " months"))
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "GOOD", durationScore, DURATION_SAFE.format(current=str(mlApplication.duration) + " months"))
        '''
        SEX
        '''
        sexScore = explanations["Sex"]

        # Only show something if it's a positive contributing factor
        if sexScore <= SAFE_THRESHOLD:
            if mlApplication.sex_male == 1:
                sex = 'Male'
            else:
                sex = 'Female'
            appendAdvice(userAdvice, "INFO", sexScore, SEX_SAFE.format(sex=sex))

        '''
        PURPOSE
        '''
        purposeScore = explanations["Purpose"]
        match purposeScore:
            case x if x >= RISK_THRESHOLD:
                appendAdvice(userAdvice, "INFO", purposeScore, PURPOSE_RISK)
            case x if x <= SAFE_THRESHOLD:
                appendAdvice(userAdvice, "INFO", purposeScore, PURPOSE_SAFE)

        '''
        Empty Array Fallback
        '''
        if userAdvice["GOOD"] == []:
            if prediction <= 0.4:
                appendAdvice(userAdvice, "GOOD", 0, "Your loan application is solid all-around.")
            else:
                appendAdvice(userAdvice, "GOOD", 0, "Adjustments to your current loan application or financial situation may aid in getting it approved. Reach out to your financial advisor for personalized and professional guidance.")

        if userAdvice["BAD"] == []:
            if prediction <= 0.4:
                appendAdvice(userAdvice, "BAD", 0, "None")
            else:
                appendAdvice(userAdvice, "BAD", 0, "Your loan application does not have any obviously negative factors. For next steps, we reccomend reaching out to your financial advisor for personalized and professional guidance.")

        if userAdvice["INFO"] == []:
            appendAdvice(userAdvice, "INFO", 0, "No additional insights found for your loan application. If you'd like, you can reach out to your financial advisor for personalized and professional guidance.")

        return userAdvice


def calculateScoreDiff(prediction, newPrediction):
    return round((prediction - newPrediction) * 100, 1)


def appendAdvice(userAdvice, adviceType, score, displayStr):
    userAdvice[adviceType].append((score, displayStr))
