import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

// PrimeNG
import { InputNumberModule } from 'primeng/inputnumber';
import { SelectModule } from 'primeng/select';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

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
    ToastModule,
  ],
  providers: [MessageService],
  templateUrl: './loan-application-page.html',
  styleUrls: ['./loan-application-page.scss'],
})
export class LoanApplicationPage {
  form: FormGroup;
  submitted = false;

  purposeOptions: SelectOption[] = [
    { label: 'Automobile / Vehicle', value: 'car' },
    { label: 'Furniture & Equipment', value: 'furniture/equipment' },
    { label: 'Radio / Television', value: 'radio/TV' },
    { label: 'Domestic Appliances', value: 'domestic appliances' },
    { label: 'Home Repairs', value: 'repairs' },
    { label: 'Education', value: 'education' },
    { label: 'Business', value: 'business' },
    { label: 'Vacation / Other', value: 'vacation/others' },
  ];

  employmentOptions: SelectOption[] = [
    { label: 'Unemployed', value: 'unemployed' },
    { label: 'Unskilled – Employed', value: 'unskilled - employed' },
    { label: 'Skilled Employee / Official', value: 'skilled employee / official' },
    { label: 'Management / Self-Employed / Highly Qualified', value: 'management / self-employed / highly qualified employee / officer' },
  ];

  housingOptions: SelectOption[] = [
    { label: 'Renting', value: 'rent' },
    { label: 'Own Home', value: 'own' },
    { label: 'Free Housing', value: 'free' },
  ];

  sexOptions: SelectOption[] = [
    { label: 'Male', value: 'male' },
    { label: 'Female', value: 'female' },
  ];

  checkingOptions: SelectOption[] = [
    { label: 'Negative Balance', value: 'negative_balance' },
    { label: 'Less than $200', value: 'less_than_200' },
    { label: '$200 – $2,000', value: '200_to_2000' },
    { label: 'No Checking Account', value: 'no_checking_account' },
  ];

  savingsOptions: SelectOption[] = [
    { label: 'No Savings Account', value: 'no_savings_account' },
    { label: 'Less than $500', value: 'less_than_500' },
    { label: '$500 – $2,500', value: '500_to_2500' },
    { label: '$2,500 – $10,000', value: '2500_to_10k' },
    { label: 'Over $10,000', value: 'over_10k' },
  ];

  constructor(private fb: FormBuilder, private messageService: MessageService) {
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
  }

  isInvalid(field: string): boolean {
    const ctrl = this.form.get(field);
    return !!ctrl && ctrl.invalid && (ctrl.dirty || ctrl.touched || this.submitted);
  }

  onSubmit(): void {
    this.submitted = true;
    if (this.form.valid) {
      console.log('Loan Application Payload:', this.form.value);
      this.messageService.add({
        severity: 'success',
        summary: 'Application Submitted',
        detail: 'Your loan application has been received.',
      });
    } else {
      this.form.markAllAsTouched();
      this.messageService.add({
        severity: 'warn',
        summary: 'Incomplete Form',
        detail: 'Please fill in all required fields.',
      });
    }
  }

  onReset(): void {
    this.submitted = false;
    this.form.reset();
  }
}