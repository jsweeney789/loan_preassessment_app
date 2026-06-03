import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AccordionModule } from 'primeng/accordion';
import { LoanApplication } from '../../types/LoanApplication';

@Component({
  selector: 'app-summary-accordion',
  imports: [CommonModule, AccordionModule],
  templateUrl: './summaryAccordion.html',
  styleUrl: './summaryAccordion.scss',
})
export class SummaryAccordion {
  @Input() application!: LoanApplication;
}
