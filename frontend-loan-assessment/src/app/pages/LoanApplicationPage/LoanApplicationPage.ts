import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

// PrimeNG
import { InputNumberModule } from 'primeng/inputnumber';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';

import { LoanApplication } from '../../types/LoanApplication';
import * as LoanEnums from '../../types/LoanApplication.enums';
import { LoanApplicationService } from '../../services/LoanApplicationService';
import { ApplicationResultService } from '../../services/ApplicationResultService';
import { Router } from '@angular/router';
import { ApplicationResult } from '../../types/ApplicationResult';
import { ApplicationHistoryDrawer } from '../../components/ApplicationHistoryDrawer/ApplicationHistoryDrawer';
import { AuthService } from '../../services/AuthService';
import { environment } from '../../../environments/environment';


interface SelectOption {
  label: string;
  value: string;
}

@Component({
  selector: 'app-loan-application-page',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    InputNumberModule,
    SelectModule,
    ButtonModule,
    CardModule,
    DividerModule,
    ApplicationHistoryDrawer
  ],
  providers: [],
  templateUrl: './LoanApplicationPage.html',
  styleUrls: ['./LoanApplicationPage.scss'],
})
export class LoanApplicationPage implements OnInit {
  form: FormGroup;
  submitted = false;

  purposeOptions: SelectOption[] = Object.values(LoanEnums.LoanPurpose).map(value => ({
    label: LoanEnums.LoanPurposeLabels[value],
    value,
  }));

  sexOptions: SelectOption[] = Object.values(LoanEnums.Sex).map(value => ({
    label: LoanEnums.SexLabels[value],
    value,
  }));

  employmentOptions: SelectOption[] = Object.values(LoanEnums.EmploymentStatus).map(value => ({
    label: LoanEnums.EmploymentStatusLabels[value],
    value,
  }));

  housingOptions: SelectOption[] = Object.values(LoanEnums.HousingStatus).map(value => ({
    label: LoanEnums.HousingStatusLabels[value],
    value,
  }));

  constructor(
    private fb: FormBuilder, 
    private loanApplicationService: LoanApplicationService,
    private applicationResultService: ApplicationResultService,
    private router: Router,
    public authService: AuthService
  ) {
    this.form = this.fb.group({
      // Personal
      age:          [null, [Validators.required, Validators.min(1)]],
      sex:          [null, Validators.required],
      job:          [null, Validators.required],
      housing:      [null, Validators.required],
      // Financial
      checkingAcc:  [null, Validators.required],
      savingAcc:    [null, Validators.required],
      // Loan
      creditAmount: [null, [Validators.required, Validators.min(1)]],
      duration:     [null, [Validators.required, Validators.min(1)]],
      purpose:      [null, Validators.required],
    });

    // Restore form data if available
    this.restoreFormData();
  }

  ngOnInit(): void {
    window.scrollTo(0, 0); // Scroll to the top when the component is initialized
    this.authService.checkAuth().subscribe();
  }

  restoreFormData(): void {
    const savedData = this.loanApplicationService.getLoanApplicationData();
    if (savedData) {
      this.form.patchValue(savedData);
    }
  }

  isInvalid(field: string): boolean {
    const ctrl = this.form.get(field);
    return !!ctrl && ctrl.invalid && (ctrl.dirty || ctrl.touched || this.submitted);
  }

  onSubmit(): void {
    this.submitted = true;
    if (this.form.valid) {
      const loanApp: LoanApplication = { ...this.form.value }
      console.log('Form Data:', loanApp);

      this.handleSubmitLoanApplication(loanApp)

    } else {
      this.form.markAllAsTouched();
    }
  }

  onReset(): void {
    this.submitted = false;
    this.form.reset();
    // Clear the stored data when the form is reset
    this.loanApplicationService.clearLoanApplicationData();
  }

  handleSubmitLoanApplication(loanApp: LoanApplication) {
    this.loanApplicationService.submitLoanApplication(loanApp).subscribe({
        next: (data: ApplicationResult) => {
          console.log("Payload sent: ", loanApp)
          this.applicationResultService.applicationResult.set(data);
          console.log("Response: ", data)
          this.router.navigate(['/results']);
        },
        error: (err) => {
          console.error('Failed to submit loan application.', err)
        }
      })
  }

  loginWithGoogle(): void {
      const redirect = encodeURIComponent(`${window.location.origin}/loanapplication`);
      window.location.href = `${environment.apiUrl}/auth/login?redirect=${redirect}`;
  }
}