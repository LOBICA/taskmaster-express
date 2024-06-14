import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-facebook-login',
  standalone: true,
  imports: [],
  templateUrl: './facebook-login.component.html',
  styleUrl: './facebook-login.component.scss'
})
export class FacebookLoginComponent {
  constructor(private loginService: LoginService){}

  checkStatus(): void {
    FB.getLoginStatus(({authResponse}) => {
      if (authResponse?.accessToken) {
        this.loginService.apiAuthenticate(authResponse.accessToken)
          .subscribe((jwt) => {
            localStorage.setItem('jwt', jwt.access_token);
            localStorage.setItem('refresh', jwt.refresh_token);
            this.loginService.updateStatus(true);
          })      
      } 
    });
  }
}
