import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import { LoanApplication } from '../types/LoanApplication';
import { ApplicationResult } from '../types/ApplicationResult';
import { LoanApplicationHistory } from '../types/LoanApplicationHistory';

@Injectable({
  providedIn: 'root',
})
export class LoanApplicationService {
    private loanApplicationData: LoanApplication | null = null;

    constructor(private http: HttpClient) {}
    private readonly url = `${environment.apiUrl}/api/loan-application`

    submitLoanApplication(loanApp: LoanApplication): Observable<ApplicationResult> {
        // Store the loan application data before submitting
        this.loanApplicationData = loanApp;
        return this.http
            .post<ApplicationResult>(this.url, loanApp, { withCredentials: true })
            .pipe( catchError(() => throwError(() => new Error('Failed to submit loan application for assessment.'))),
        );
    }

    // Method to retrieve the stored loan application data
    getLoanApplicationData(): LoanApplication | null {
        return this.loanApplicationData;
    }

    // Method to clear the stored loan application data
    clearLoanApplicationData(): void {
        this.loanApplicationData = null;
    }

    private readonly historyUrl = `${environment.apiUrl}/api/my-applications`

    getApplicationHistory(): Observable<LoanApplicationHistory[]> {
        return this.http
            .get<LoanApplicationHistory[]>(this.historyUrl, { withCredentials: true })
            .pipe(catchError(() => throwError(() => new Error('Failed to fetch application history.'))));
    }
}