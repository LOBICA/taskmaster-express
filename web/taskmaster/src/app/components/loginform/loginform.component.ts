import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import {
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { LoginData } from '../../models/logindata.model';
import { AnalyticsService } from '../../services/analytics.service';

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
export class LoginformComponent implements OnInit {
  @Input() disabled = false;

  @Output() loginEvent = new EventEmitter<LoginData>();

  constructor(private analytics: AnalyticsService) {}

  ngOnInit(): void {
    this.analytics.trackEvent('Login Form', 'User reached the login form', 'AUTH');
  }

  loginForm = new FormGroup({
    username: new FormControl<string>('', Validators.required),
    password: new FormControl<string>('', Validators.required),
  });

  login() {
    const loginData = {
      username: this.loginForm.value.username!,
      password: this.loginForm.value.password!,
    };
    this.loginEvent.emit(loginData);
  }
}
