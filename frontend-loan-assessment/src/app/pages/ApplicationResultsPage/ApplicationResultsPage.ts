import { Component, OnInit, ElementRef, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { ApplicationResult } from '../../types/ApplicationResult';
import { ApplicationResultService } from '../../services/ApplicationResultService';
import { Hexagon } from '../../components/Hexagon/Hexagon';
import { ButtonModule } from 'primeng/button';
import { LoanApplicationService } from '../../services/LoanApplicationService';
import { LoanApplication } from '../../types/LoanApplication';
import { AccordionModule } from 'primeng/accordion';
import { CommonModule } from '@angular/common'
import { SummaryAccordion } from "../../components/summaryAccordion/summaryAccordion";
import { ApplicationHistoryDrawer } from '../../components/ApplicationHistoryDrawer/ApplicationHistoryDrawer';
import { effect } from '@angular/core';

@Component({
  selector: 'application-results-page',
  imports: [Hexagon, ButtonModule, AccordionModule, CommonModule, SummaryAccordion, ApplicationHistoryDrawer],
  templateUrl: './ApplicationResultsPage.html',
  styleUrl: './ApplicationResultsPage.scss',
})
export class ApplicationResultsPage implements OnInit {
  result: ApplicationResult | null = null;
  application: LoanApplication | null = null;
  displayedScore: string = '0.0';
  private animationDuration: number = 1500; // 1.5 seconds

  constructor(
      private router: Router,
      private resultService: ApplicationResultService,
      private loanService: LoanApplicationService,
      private el: ElementRef,
      private cdr: ChangeDetectorRef
  ) {
      effect(() => {
          this.result = this.resultService.applicationResult();
          this.application = this.loanService.getLoanApplicationData();
          if (this.result) {
              this.sortUserAdvice();
              this.updateThemeBasedOnDecision();
              setTimeout(() => this.animateScore(), 0);
          }
      });
  }

  ngOnInit(): void {
    window.scrollTo(0, 0); // Scroll to the top when the component is initialized
  }

  updateThemeBasedOnDecision(): void {
    if (!this.result?.decision) return;
    
    const hostElement = this.el.nativeElement;
    hostElement.setAttribute('data-decision', this.result.decision);
  }

  sortUserAdvice(): void {
    if (!this.result?.userAdvice) return;

    // Sort GOOD advice from low to high
    this.result.userAdvice.GOOD.sort((a: [number, string], b: [number, string]) => a[0] - b[0]);

    // Sort BAD advice from high to low
    this.result.userAdvice.BAD.sort((a: [number, string], b: [number, string]) => b[0] - a[0]);

    // Sort INFO by highest absolute value to lowest
    this.result.userAdvice.INFO.sort((a: [number, string], b: [number, string]) => Math.abs(b[0]) - Math.abs(a[0]));
  }

  animateScore(): void {
    if (!this.result) return;

    const targetScore = (1 - this.result.prediction) * 100;
    const startTime = performance.now();

    const animate = (currentTime: number) => {
      const elapsedTime = currentTime - startTime;
      const progress = Math.min(elapsedTime / this.animationDuration, 1);

      // Stronger ease-out function to start fast and slow to a crawl
      const easedProgress = 1 - Math.pow(1 - progress, 15);
      const currentScore = targetScore * easedProgress;

      this.displayedScore = currentScore.toFixed(1);
      this.cdr.detectChanges(); // Manually trigger change detection

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        // Ensure the final value is exact
        this.displayedScore = targetScore.toFixed(1);
        this.cdr.detectChanges(); // Manually trigger change detection
      }
    };

    requestAnimationFrame(animate);
  }

  goBack(): void {
    this.router.navigate(['/loanapplication']);
  }
}

