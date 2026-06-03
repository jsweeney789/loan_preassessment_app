import { Routes } from '@angular/router';
import { LoanApplicationPage } from './pages/LoanApplicationPage/LoanApplicationPage';
import { ApplicationResultsPage } from './pages/ApplicationResultsPage/ApplicationResultsPage'
import { WelcomePage } from './pages/WelcomePage/WelcomePage';
export const routes: Routes = [
    { path: '', redirectTo: 'login', pathMatch: 'full'},
    { path: 'loanapplication', component: LoanApplicationPage},
    { path: 'results', component: ApplicationResultsPage, runGuardsAndResolvers: 'always' },
    { path: 'login', component: WelcomePage}
];
