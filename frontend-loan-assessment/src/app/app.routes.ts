import { Routes } from '@angular/router';
import { LoanApplicationPage } from './pages/LoanApplicationPage/LoanApplicationPage';
import { ApplicationResultsPage } from './pages/ApplicationResultsPage/ApplicationResultsPage'
export const routes: Routes = [
    { path: '', redirectTo: 'loanapplication', pathMatch: 'full'},
    { path: 'loanapplication', component: LoanApplicationPage},
    { path: 'results', component: ApplicationResultsPage}
];
