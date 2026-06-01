from backendLoanAssessment.schemas.LoanApplication import *
from backendLoanAssessment.services import SageMakerService
from backendLoanAssessment.constants.AdviceStrings import *
from copy import deepcopy

class AdviceService:
    def __init__(self, sagemakerService: SageMakerService):
        self.sagemaker = sagemakerService

    def generateUserAdvice(self, mlApplication, prediction, explanations):
        userAdvice = {"GOOD": [], "BAD": [], "INFO": []}

        '''
        AGE
        '''
        ageScore = explanations["Age"]
        match ageScore:
            case x if x >= 0.15:
                userAdvice["INFO"].append((ageScore, AGE_RISK.format(age=mlApplication.age)))
            case x if x <= -0.15:
                userAdvice["GOOD"].append((ageScore, AGE_SAFE.format(age=mlApplication.age)))

        '''
        JOB
        '''
        jobScore = explanations["Job"]
        match jobScore:
            case x if x >= 0.15:
                newPrediction = 0

                if mlApplication.job < 3:
                    newMlApplication = deepcopy(mlApplication)
                    newMlApplication.job += 1
                    newPrediction, _ = self.sagemaker.predictWithExplanations(
                        newMlApplication
                    )

                scoreDiff = round((prediction - newPrediction) * 100, 1)
                if scoreDiff >= 0.1:
                    userAdvice["BAD"].append(
                        (
                            jobScore,
                            JOB_RISK_POINTS.format(
                                jobPlus1=employmentStringMap[mlApplication.job + 1],
                                diff=scoreDiff,
                            ),
                        )
                    )
                else:
                    userAdvice["BAD"].append(
                        (jobScore, JOB_RISK.format(job=employmentStringMap[mlApplication.job]))
                    )

            case x if x <= -0.3:
                userAdvice["GOOD"].append(
                    (jobScore, JOB_BIG_SAFE.format(job=employmentStringMap[mlApplication.job]))
                )
            case x if x <= -0.15:
                userAdvice["GOOD"].append(
                    (jobScore, JOB_SAFE.format(job=employmentStringMap[mlApplication.job]))
                )
        return userAdvice