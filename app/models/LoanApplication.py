from pydantic import BaseModel, field_validator
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

class EmploymentStatus(str, Enum):
    unemployed = "unemployed" 
    employed = "unskilled - employed"
    highlyEmployed = "skilled employee / official"
    veryHighlyEmployed = "management / self-employed / highly qualified employee / officer"

    employmentNumericMap = {
        "unemployed":           1,                                             # A171
        "unskilled":            2,                                             # A172
        "skilled employee / official": 3,                                      # A173
        "management / self-employed / highly qualified employee / officer": 4  # A174
    }
# the original dataset has resident/non-resident of germany, removed as this would run into fair lending law issues in the US and still maps to a reasonable understanding of a person maybe


class HomeOwnership(str, Enum):
    rent = "rent"
    own = "own"
    free = "free"

    homeOwnershipNumericMap = {
        "rent": 1,  # A151
        "own": 2,   # A152
        "free": 3   # A153
    }

class Sex(str, Enum):
    male = "male"
    female = "female"

    sexNumericMap = {
        "male": 1,
        "female": 2
    }

class CheckingAccountStatus(str, Enum):
    overdraft = "negative_balance"
    low = "less_than_200"          # under $200
    moderate = "200_to_2000"       # $200-$2000, or has direct deposit
    none = "no_checking_account"

    checkingAcctNumericMap = {
        "negative_balance": 1,      # A11
        "less_than_250": 2,         # A12
        "250_to_2000": 3,           # A13
        "no_checking_account": 4    # A14
    }


class SavingsAccountStatus(str, Enum):
    none = "no_savings_account"
    little = "less_than_500"       # under $500 — below the "one emergency away from crisis" line
    moderate = "500_to_2500"       # $500-$2,500
    quite_rich = "2500_to_10k"     # $2,500-$10,000
    rich = "over_10k"              # $10,000+

    savingsAcctNumericMap = {
        "less_than_500": 1,        # A61
        "500_to_2500": 2,          # A62
        "2500_to_10k": 3,          # A63
        "over_10k": 4,             # A64
        "no_savings_account": 5,   # A65
    }


class LoanApplication:
    age: int
    sex: Sex
    job: EmploymentStatus
    housing: HomeOwnership
    checkingAcc: CheckingAccountStatus
    savingAcc: SavingsAccountStatus
    creditAmount: int
    duration: int
    purpose: LoanPurpose