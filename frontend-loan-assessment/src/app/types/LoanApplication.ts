import { EmploymentStatus, HousingStatus, LoanPurpose, Sex } from "./LoanApplication.enums";

export interface LoanApplication {
    age: number,
    sex: Sex,
    job: EmploymentStatus,
    housing: HousingStatus,
    checkingAcc: number,
    savingAcc: number,
    creditAmount: number,
    duration: number,
    purpose: LoanPurpose
}

