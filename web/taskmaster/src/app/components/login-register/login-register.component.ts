import { Component } from '@angular/core';
import { MatTabsModule } from '@angular/material/tabs';
import { LoginformComponent } from '../loginform/loginform.component';
import { RegisterformComponent } from '../registerform/registerform.component';

@Component({
  selector: 'app-login-register',
  standalone: true,
  imports: [
    MatTabsModule,
    LoginformComponent,
    RegisterformComponent,
  ],
  templateUrl: './login-register.component.html',
  styleUrl: './login-register.component.scss'
})
export class LoginRegisterComponent {

}
