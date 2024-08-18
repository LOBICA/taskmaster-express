import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatTabsModule } from '@angular/material/tabs';
import { Subject, takeUntil } from 'rxjs';
import { LoginformComponent } from './components/loginform/loginform.component';
import { RegisterformComponent } from './components/registerform/registerform.component';
import { FacebookLoginComponent } from './components/facebook-login/facebook-login.component';
import { SubscriptionBannerComponent } from './components/subscription-banner/subscription-banner.component';
import { TasksComponent } from './components/tasks/tasks.component';
import { ChatComponent } from './components/chat/chat.component';
import { LoginService } from './services/login.service';
import { UserService } from './services/user.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatTabsModule,
    LoginformComponent,
    RegisterformComponent,
    FacebookLoginComponent,
    SubscriptionBannerComponent,
    TasksComponent,
    ChatComponent,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit, OnDestroy{
  title = 'Help It Done!';
  user = 'Guest';
  loggedIn = false;
  unsubscribe$ = new Subject<void>();

  constructor(
    private router: Router,
    private loginService: LoginService,
    private userService: UserService,
  ) {}

  ngOnInit(): void {
      this.loginService.loginStatus$.pipe(takeUntil(this.unsubscribe$)).subscribe((status) => {
        this.loggedIn = status;
        this.loadUserInfo();
      });
      const storedToken = localStorage.getItem('jwt');
      if (storedToken) {
        this.loginService.updateStatus(true);
      } else {
        this.loadUserInfo();
      }
  }

  ngOnDestroy(): void {
      this.unsubscribe$.next();
      this.unsubscribe$.complete();
  }

  loadUserInfo() {
    if (!this.loggedIn) {
      this.user = 'Guest';
    }
    else {
      this.userService.getCurrentUser().subscribe((user) => {
        this.user = user.name ?? 'Anon';
      });
    }
  }

  logout() {
    this.loginService.logout();
    this.router.navigate(['/']);
  }
}
