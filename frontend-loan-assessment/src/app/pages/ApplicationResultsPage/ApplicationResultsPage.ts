import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApplicationResult } from '../../types/ApplicationResult';
import { ApplicationResultService } from '../../services/ApplicationResultService';
import { Hexagon } from '../../componenets/hexagon/hexagon';
import { KeyValuePipe } from '@angular/common';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'application-results-page',
  imports: [ Hexagon, KeyValuePipe, ButtonModule ],
  templateUrl: './ApplicationResultsPage.html',
  styleUrl: './ApplicationResultsPage.scss',
})
export class ApplicationResultsPage {
  result: ApplicationResult | null = null;

  constructor(
    private router: Router,
    private resultService: ApplicationResultService
  ) {
    this.result = this.resultService.applicationResult;
    if (this.result) {
      this.sortUserAdvice();
    }
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

  goBack(): void {
    this.router.navigate(['/loanapplication']);
  }
}
