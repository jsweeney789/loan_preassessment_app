import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DrawerModule } from 'primeng/drawer';
import { ButtonModule } from 'primeng/button';
import { LoanApplicationService } from '../../services/LoanApplicationService';
import { ApplicationResultService } from '../../services/ApplicationResultService';
import { LoanApplicationHistory } from '../../types/LoanApplicationHistory';
import { ChangeDetectorRef } from '@angular/core';
import { LoanApplication } from '../../types/LoanApplication';
import { ApplicationResult } from '../../types/ApplicationResult';

@Component({
  selector: 'app-history-drawer',
  standalone: true,
  imports: [CommonModule, DrawerModule, ButtonModule],
  templateUrl: './ApplicationHistoryDrawer.html',
  styleUrl: './ApplicationHistoryDrawer.scss'
})
export class ApplicationHistoryDrawer implements OnInit, OnDestroy {
  visible = false;
  history: LoanApplicationHistory[] = [];
  loading = false;
  private pendingNavigation = false;

  constructor(
    private loanService: LoanApplicationService,
    private resultService: ApplicationResultService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {}

  ngOnDestroy(): void {
    // Force remove any orphaned PrimeNG overlay masks on the body
    document.querySelectorAll('.p-drawer-mask, .p-overlay-mask').forEach(el => el.remove());
    document.body.classList.remove('p-overflow-hidden');
  }

  open(): void {
    this.visible = true;
    this.loading = true;
    this.loanService.getApplicationHistory().subscribe({
      next: (data) => {
        this.history = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  selectApplication(item: LoanApplicationHistory): void {
      if (!item.result) return;

      const rawResult = item.result as any;
      const mappedResult: ApplicationResult = {
          prediction: rawResult.prediction,
          decision: rawResult.decision,
          userAdvice: rawResult.user_advice,
          explanations: rawResult.explanations
      };
      this.resultService.applicationResult.set(mappedResult)

      const loanApp: LoanApplication = {
          age: item.age,
          sex: item.sex as any,
          job: item.job as any,
          housing: item.housing as any,
          checkingAcc: item.checking_acc,
          savingAcc: item.saving_acc,
          creditAmount: item.credit_amount,
          duration: item.duration,
          purpose: item.purpose as any
      };

      this.loanService.setLoanApplicationData(loanApp);
      this.pendingNavigation = true;
      this.visible = false;
      setTimeout(() => this.router.navigate(['/results']));
  }

  getDecisionClass(decision: string): string {
    if (decision.includes('Confident Approval')) return 'decision-confident-approval';
    if (decision.includes('Likely Approval')) return 'decision-likely-approval';
    if (decision.includes('Unsure')) return 'decision-unsure';
    if (decision.includes('Likely Disapproval')) return 'decision-likely-disapproval';
    return 'decision-confident-disapproval';
  }

  onDrawerHidden(): void {
    if (this.pendingNavigation) {
        this.pendingNavigation = false;
        this.router.navigate(['/results']);
    }
  }
}

