export enum LoanPurpose {
    Car = "car",
    FurnitureEquipment = "furniture/equipment",
    RadioTV = "radio/TV",
    DomesticApplicanes = "domestic appliances",
    Repairs = "repairs",
    Education = "education",
    Business = "business",
    VacationOther = "vacation/other"
}

export const LoanPurposeLabels: Record<LoanPurpose, string> = {
  [LoanPurpose.Car]: 'Automobile / Vehicle',
  [LoanPurpose.FurnitureEquipment]: 'Furniture & Equipment',
  [LoanPurpose.RadioTV]: 'Radio / Television',
  [LoanPurpose.DomesticApplicanes]: 'Domestic Appliances',
  [LoanPurpose.Repairs]: 'Home Repairs',
  [LoanPurpose.Education]: 'Education',
  [LoanPurpose.Business]: 'Business',
  [LoanPurpose.VacationOther]: 'Vacation / Other',
};

export enum Sex {
    Male = "male",
    Female = "female"
}  

export const SexLabels: Record<Sex, string> = {
  [Sex.Male]: 'Male',
  [Sex.Female]: 'Female',
};

export enum EmploymentStatus {
    Unemployed = "unemployed",
    Unskilled = "unskilled",
    Skilled = "skilled employee / official",
    HighlySkilled = "management / self-employed / highly qualified employee / officer"
}

export const EmploymentStatusLabels: Record<EmploymentStatus, string> = {
  [EmploymentStatus.Unemployed]: 'Unemployed',
  [EmploymentStatus.Unskilled]: 'Unskilled – Employed',
  [EmploymentStatus.Skilled]: 'Skilled Employee / Official',
  [EmploymentStatus.HighlySkilled]: 'Management / Self-Employed / Highly Qualified',
};

export enum HousingStatus {
    Free = "free",
    Rent = "rent",
    Own = "own"
}

export const HousingStatusLabels: Record<HousingStatus, string> = {
  [HousingStatus.Free]: 'Free Housing',
  [HousingStatus.Rent]: 'Renting',
  [HousingStatus.Own]: 'Own Home',
};