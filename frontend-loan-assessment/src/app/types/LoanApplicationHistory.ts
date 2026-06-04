import { ApplicationResult } from './ApplicationResult';

export interface LoanApplicationHistory {
    id: number;
    age: number;
    sex: string;
    job: string;
    housing: string;
    checking_acc: number;
    saving_acc: number;
    credit_amount: number;
    duration: number;
    purpose: string;
    created_at: string;
    result: ApplicationResult | null;
}