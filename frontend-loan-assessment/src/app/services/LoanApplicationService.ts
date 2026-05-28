import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, throwError } from 'rxjs';
import { environment } from '../../environments/environment';
import { LoanApplication } from '../types/LoanApplication';

@Injectable({
  providedIn: 'root',
})
export class LoanApplicationService {
    constructor(private http: HttpClient) {}
    private readonly url = `${environment.apiUrl}/api/loan-application`

    submitLoanApplication(loanApp: LoanApplication): Observable<LoanApplication> {
        return this.http
            .post<LoanApplication>(this.url, loanApp)
            .pipe( catchError(() => throwError(() => new Error('Failed to submit loan application for assessment.'))),
        );
    }
}