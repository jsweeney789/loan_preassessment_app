from pydantic import BaseModel, Field, ConfigDict, field_validator
from enum import Enum

class LoanPurpose(str, Enum):
    auto = "car"
    furniture_equipment = "furniture/equipment"
    radio_tv = "radio/TV"
    domestic_appliances = "domestic appliances"
    repairs = "repairs"
    education = "education"
    business = "business"
    vacation_others = "vacation/others"
    @staticmethod
    def encodePurpose(purpose: LoanPurpose) -> dict:
        return {
        "Purpose_car":                  1 if purpose == LoanPurpose.auto else 0,
        "Purpose_domestic appliances":  1 if purpose == LoanPurpose.domestic_appliances else 0,
        "Purpose_education":            1 if purpose == LoanPurpose.education else 0,
        "Purpose_furniture/equipment":  1 if purpose == LoanPurpose.furniture_equipment else 0,
        "Purpose_radio/TV":             1 if purpose == LoanPurpose.radio_tv else 0,
        "Purpose_repairs":              1 if purpose == LoanPurpose.repairs else 0,
        "Purpose_vacation/others":      1 if purpose == LoanPurpose.vacation_others else 0,
    }

class EmploymentStatus(str, Enum):
    unemployed = "unemployed" 
    employed = "unskilled"
    highlyEmployed = "skilled employee / official"
    veryHighlyEmployed = "management / self-employed / highly qualified employee / officer"

employmentNumericMap = {
    "unemployed":           0,                                             # A171
    "unskilled":            1,                                             # A172
    "skilled employee / official": 2,                                      # A173
    "management / self-employed / highly qualified employee / officer": 3  # A174
}
# the original dataset has resident/non-resident of germany, removed as this would run into fair lending law issues in the US and still maps to a reasonable understanding of a person maybe


class HomeOwnership(str, Enum):
    rent = "rent"
    own = "own"
    free = "free"

homeOwnershipNumericMap = {
    "rent": 1,  # A151
    "own": 2,   # A152
    "free": 0   # A153
}

class Sex(str, Enum):
    male = "male"
    female = "female"

sexNumericMap = {
    "male": 1,
    "female": 0
}

class CheckingAccountStatus(int, Enum):
    NA = 0
    little = 1          
    moderate = 2    
    rich = 4
    @staticmethod
    def classify(amount: float) -> CheckingAccountStatus:
        if amount < 1000:
            return CheckingAccountStatus.little
        elif amount < 5000:
            return CheckingAccountStatus.moderate
        else:
            return CheckingAccountStatus.rich
        # else:
        #     return CheckingAccountStatus.NA  # no checking account bucket doesn't apply here, consider renaming


class SavingsAccountStatus(int, Enum):
    NA = 0
    little = 1
    moderate = 2
    quite_rich = 3
    rich = 4
    @staticmethod
    def classify(amount: float) -> SavingsAccountStatus:
        if amount <= 0:
            return SavingsAccountStatus.NA
        elif amount < 1000:
            return SavingsAccountStatus.little
        elif amount < 10000: # a noteworthy target for moderate is that the median savings account balance for all families was 8,000 in 2022
            return SavingsAccountStatus.moderate # https://www.usnews.com/banking/articles/the-average-savings-account-balance
        elif amount < 50000:
            return SavingsAccountStatus.quite_rich
        else:
            return SavingsAccountStatus.rich


class LoanApplication(BaseModel):
    age: int
    sex: Sex
    job: EmploymentStatus
    housing: HomeOwnership
    checkingAcc: int
    savingAcc: int
    creditAmount: int
    duration: int
    purpose: LoanPurpose
    @field_validator("age", "duration", "creditAmount")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be greater than zero")
        return v

# Field allows us to alias the python properties exactly to what the ML expects by our one-hot encoding, which had spaces occasionally
class MLLoanApplication(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    age: int = Field(alias="Age")
    job: int = Field(alias="Job")
    housing: int = Field(alias="Housing")
    savingAcc: int = Field(alias="Saving accounts")
    checkingAcc: int = Field(alias="Checking account")
    creditAmount: int = Field(alias="Credit amount")
    duration: int = Field(alias="Duration")
    sex_male: int = Field(alias="Sex_male")
    purpose_car: int = Field(alias="Purpose_car")
    purpose_domestic_appliances: int = Field(alias="Purpose_domestic appliances")
    purpose_education: int = Field(alias="Purpose_education")
    purpose_furniture_equipment: int = Field(alias="Purpose_furniture/equipment")
    purpose_radio_tv: int = Field(alias="Purpose_radio/TV")
    purpose_repairs: int = Field(alias="Purpose_repairs")
    purpose_vacation_others: int = Field(alias="Purpose_vacation/others")

class LoanDecision(str, Enum):
    confident_approval = "Confident Approval"
    likely_approval = "Likely Approval"
    unsure = "Unsure"
    likely_disapproval = "Likely Disapproval"
    confident_disapproval = "Confident Disapproval"

class ApplicationResult(BaseModel):
    prediction: float
    decision: str
    explanations: dict[str, float]