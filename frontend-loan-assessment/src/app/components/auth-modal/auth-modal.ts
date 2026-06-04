import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/AuthService';

@Component({
  selector: 'app-auth-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './auth-modal.html',
  styleUrls: ['./auth-modal.scss']
})
export class AuthModalComponent {
  @Output() closed = new EventEmitter<void>();
  @Output() authenticated = new EventEmitter<void>();

  activeTab: 'login' | 'register' = 'login';
  email = '';
  password = '';
  error = '';
  loading = false;

  constructor(private authService: AuthService) {}

  switchTab(tab: 'login' | 'register') {
    this.activeTab = tab;
    this.error = '';
  }

  submit() {
    this.error = '';
    this.loading = true;

    const request$ = this.activeTab === 'login'
      ? this.authService.login(this.email, this.password)
      : this.authService.register(this.email, this.password);

    request$.subscribe({
      next: () => {
        this.loading = false;
        this.authenticated.emit();
        this.closed.emit();
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Something went wrong';
      }
    });
  }

  googleLogin() {
    this.authService.loginWithGoogle();
  }

  close() {
    this.closed.emit();
  }
}