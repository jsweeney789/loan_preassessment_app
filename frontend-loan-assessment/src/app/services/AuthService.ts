import { HttpClient } from "@angular/common/http";
import { Injectable, signal } from "@angular/core";
import { map, Observable, tap } from "rxjs";
import { environment } from "../../environments/environment";
import { Router } from "@angular/router";

@Injectable({ providedIn: 'root' })
export class AuthService {
  isAuthenticated = signal(false);

  constructor(private http: HttpClient, 
    private router: Router
  ) {}

    checkAuth(): Observable<void> {
        return this.http.get<{authenticated: boolean}>(`${environment.apiUrl}/auth/status`, { withCredentials: true }).pipe(
        tap(res => this.isAuthenticated.set(res.authenticated)),
        map(() => void 0)
        );
    }

    logout(): void {
        this.http.get(`${environment.apiUrl}/auth/logout`, { withCredentials: true }).subscribe({
            next: () => {
                this.isAuthenticated.set(false);
                this.router.navigate(['/loanapplication']);
            }
        });
    }
}