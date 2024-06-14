import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-facebook-login',
  standalone: true,
  imports: [],
  templateUrl: './facebook-login.component.html',
  styleUrl: './facebook-login.component.scss'
})
export class FacebookLoginComponent implements OnInit{
  constructor(private loginService: LoginService){}

  ngOnInit(): void {
  }
}
