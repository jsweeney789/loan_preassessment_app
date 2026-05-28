import { Injectable } from "@angular/core";
import { ApplicationResult } from "../types/ApplicationResult";

@Injectable({ providedIn: 'root' })
export class ApplicationResultService {
  applicationResult: ApplicationResult | null = null;
}