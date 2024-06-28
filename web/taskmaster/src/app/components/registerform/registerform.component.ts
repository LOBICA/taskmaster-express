import { Component } from '@angular/core';
import { FormControl, FormGroup, FormGroupDirective, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { finalize } from 'rxjs';
import { UserService } from '../../services/user.service';
import { SnackBarService } from '../../services/snackBar.service';
import { User } from '../../models/user.model';
import { MatchValue } from '../../utils/match-value.validator';

@Component({
  selector: 'app-registerform',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
  ],
  templateUrl: './registerform.component.html',
  styleUrl: './registerform.component.scss'
})
export class RegisterformComponent {
  disabled = false;

  registerForm = new FormGroup({
    name: new FormControl<string>('', Validators.required),
    email: new FormControl<string>('', Validators.required),
    password: new FormControl<string>('', Validators.required),
    confirmPassword: new FormControl<string>('', Validators.required)
  }, {
    validators: MatchValue('password', 'confirmPassword')
  });

  constructor(
    private userService: UserService,
    private snackBarService: SnackBarService,
  ) {}

  register(formDirective: FormGroupDirective) {
    const user = new User(
      null,
      this.registerForm.value.name!,
      this.registerForm.value.email!,
      this.registerForm.value.password!
    );
    this.disabled = true;

    this.userService.registerUser(user).pipe(
    finalize(() => {
      this.disabled = false;
    })).subscribe({
      next: () => {
        this.snackBarService.openSnackbar('Registration Successful', 'success');
        this.registerForm.reset();
        formDirective.resetForm();
      },
      error: () => {
        this.snackBarService.openSnackbar('Registration Failed', 'error');
      },
    });
  }
}
