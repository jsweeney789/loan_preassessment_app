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
  result: ApplicationResult | null

  constructor(
    private router: Router,
    private resultService: ApplicationResultService
  ) {
    this.result = this.resultService.applicationResult
  }


  goBack(): void {
    this.router.navigate(['/loanapplication']);
  }
}
