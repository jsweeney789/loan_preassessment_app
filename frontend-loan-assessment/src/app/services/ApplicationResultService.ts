import { Injectable, signal } from "@angular/core";
import { ApplicationResult } from "../types/ApplicationResult";

@Injectable({ providedIn: 'root' })
export class ApplicationResultService {
    applicationResult = signal<ApplicationResult | null>(null);
}