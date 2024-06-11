import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { JWT } from '../models/jwt.model';
import { LoginData } from '../models/logindata.model';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  constructor(private http: HttpClient) {}

  login(loginData: LoginData): Observable<JWT> {
    return this.http.post<JWT>(environment.apiUrl + '/token', loginData);
  }
}
