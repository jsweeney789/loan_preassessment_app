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

      login(email: string, password: string): Observable<void> {
      return this.http.post<void>(
        `${environment.apiUrl}/auth/login/password`,
        { email, password },
        { withCredentials: true }
      ).pipe(tap(() => this.isAuthenticated.set(true)));
    }

    register(email: string, password: string): Observable<void> {
      return this.http.post<void>(
        `${environment.apiUrl}/auth/register`,
        { email, password },
        { withCredentials: true }
      ).pipe(tap(() => this.isAuthenticated.set(true)));
    }

      loginWithGoogle(): void {
          const redirect = encodeURIComponent(`${window.location.origin}/loanapplication`);
          window.location.href = `${environment.apiUrl}/auth/login?redirect=${redirect}`;
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