import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { UserService } from '../../services/user.service';
import { LoginService } from '../../services/login.service';
import { User } from '../../models/user.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatCardModule, MatButtonModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent {
  user: User | undefined | null;

  constructor(
    private userService: UserService,
    private loginService: LoginService,
    private router: Router,
  ) {
    this.userService.getCurrentUser().subscribe(user => {
      this.user = user;
    });
  }

  deleteAccount(): void {
    this.userService.deleteCurrentUser().subscribe(() => {
      this.user = null;
      this.loginService.logout();
      this.router.navigate(['/']);
    });
  }
}
