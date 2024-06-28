import { Component } from '@angular/core';
import { FormControl, FormGroup, FormGroupDirective, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { EMPTY, catchError } from 'rxjs';
import { UserService } from '../../services/user.service';
import { SnackBarService } from '../../services/snackBar.service';
import { User } from '../../models/user.model';

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
      catchError(() => {
        this.snackBarService.openSnackbar('Registration Failed', 'error');
        return EMPTY;
      })
    ).subscribe(() => {
      this.disabled = false
      this.snackBarService.openSnackbar('Registration Successful', 'success');
      this.registerForm.reset();
      formDirective.resetForm();
    });
  }
}
