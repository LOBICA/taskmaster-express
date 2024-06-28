import { Component } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { finalize } from 'rxjs';
import { LoginData } from '../../models/logindata.model';
import { AnalyticsService } from '../../services/analytics.service';
import { SnackBarService } from '../../services/snackBar.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-loginform',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
  ],
  templateUrl: './loginform.component.html',
  styleUrl: './loginform.component.scss',
})
export class LoginformComponent {
  disabled = false;

  loginForm = new FormGroup({
    username: new FormControl<string>('', Validators.required),
    password: new FormControl<string>('', Validators.required),
  });
  
  constructor(
    private loginService: LoginService,
    private snackBarService: SnackBarService,
    private analytics: AnalyticsService
  ) {}
  
  ngOnInit(): void {
    this.analytics.trackEvent('Login Form', 'User reached the login form', 'AUTH');
  }

  login() {
    const loginData = new LoginData(
      this.loginForm.value.username!,
      this.loginForm.value.password!
    );
    this.disabled = true;
    this.loginService.login(loginData).pipe(
    finalize(() => {
      this.disabled = false;
    })).subscribe({
      next: (jwt) => {
        localStorage.setItem('jwt', jwt.access_token);
        localStorage.setItem('refresh', jwt.refresh_token);
        this.loginService.updateStatus(true);
        this.snackBarService.openSnackbar('Login Successful', 'success');
      },
      error: () => {
        this.snackBarService.openSnackbar('Login Failed', 'error');
      },
    });
  }
}
