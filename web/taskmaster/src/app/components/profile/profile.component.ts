import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { UserService } from '../../services/user.service';
import { LoginService } from '../../services/login.service';
import { User } from '../../models/user.model';
import { Router } from '@angular/router';
import { ConfirmDialogComponent } from '../confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, MatDialogModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss'
})
export class ProfileComponent {
  user: User | undefined | null;

  constructor(
    private userService: UserService,
    private loginService: LoginService,
    private router: Router,
    private dialog: MatDialog
  ) {
    this.userService.getCurrentUser().subscribe(user => {
      this.user = user;
    });
  }

  deleteAccount(): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete user',
        description: 'This will delete all information about the current user',
        buttons: {
          cancelTitle: 'Cancel',
          confirmTitle: 'Confirm'
        },
        buttonColor: '#880808'
      }
    });

    dialogRef.afterClosed().subscribe((confirm) => {
      if (confirm) {
        this.userService.deleteCurrentUser().subscribe(() => {
          this.user = null;
          this.loginService.logout();
          this.router.navigate(['/']);
        });
      }
    })
  }
}
