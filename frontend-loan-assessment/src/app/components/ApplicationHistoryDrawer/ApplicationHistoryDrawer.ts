import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { DrawerModule } from 'primeng/drawer';
import { ButtonModule } from 'primeng/button';
import { LoanApplicationService } from '../../services/LoanApplicationService';
import { ApplicationResultService } from '../../services/ApplicationResultService';
import { LoanApplicationHistory } from '../../types/LoanApplicationHistory';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-history-drawer',
  standalone: true,
  imports: [CommonModule, DrawerModule, ButtonModule],
  templateUrl: './ApplicationHistoryDrawer.html',
  styleUrl: './ApplicationHistoryDrawer.scss'
})
export class ApplicationHistoryDrawer implements OnInit {
  visible = false;
  history: LoanApplicationHistory[] = [];
  loading = false;

  constructor(
    private loanService: LoanApplicationService,
    private resultService: ApplicationResultService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {}

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
    this.resultService.applicationResult = item.result;
    this.visible = false;
    this.router.navigate(['/results']);
  }

  getDecisionClass(decision: string): string {
    if (decision.includes('Confident Approval')) return 'decision-confident-approval';
    if (decision.includes('Likely Approval')) return 'decision-likely-approval';
    if (decision.includes('Unsure')) return 'decision-unsure';
    if (decision.includes('Likely Disapproval')) return 'decision-likely-disapproval';
    return 'decision-confident-disapproval';
  }
}