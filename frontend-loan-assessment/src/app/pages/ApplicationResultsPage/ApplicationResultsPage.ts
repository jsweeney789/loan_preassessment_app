import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'application-results-page',
  imports: [],
  templateUrl: './ApplicationResultsPage.html',
  styleUrl: './ApplicationResultsPage.css',
})
export class ApplicationResultsPage {
  decision: string;

  constructor(private router: Router) {
    this.decision = this.router.getCurrentNavigation()?.extras.state?.['decision'];
  }

  goBack(): void {
    this.router.navigate(['/loan-application']);
  }
}
