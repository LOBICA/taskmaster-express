import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { environment } from '../../environments/environment';
import { JWT } from '../models/jwt.model';
import { LoginData } from '../models/logindata.model';
import { SnackBarService } from './snackBar.service';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  loginStatus$ = new BehaviorSubject<boolean>(false);
  tokenRefreshing = false;
  refreshedToken$ = new Subject<string | null>();

  constructor(private http: HttpClient, private snackBarService: SnackBarService) {}

  apiAuthenticate(accessToken: string) {
    return this.http.post<JWT>(`${environment.apiUrl}/fb_login`, { accessToken })
  }

  login(loginData: LoginData): Observable<JWT> {
    let headers = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');

    const body = new URLSearchParams();
    body.set('username', loginData.username);
    body.set('password', loginData.password);

    return this.http.post<JWT>(environment.apiUrl + '/token', body.toString(), {
      headers
    });
  }

  getRefreshedToken(refreshToken: string): Observable<JWT> {
    return this.http.post<JWT>(environment.apiUrl + '/refresh', { refreshToken })
  }

  updateStatus(status: boolean) {
    this.loginStatus$.next(status);
  }

  logout(): void {
    FB.api('/me/permissions', 'delete', {}, () => FB.logout());
    FB.logout();
    localStorage.removeItem('jwt');
    localStorage.removeItem('refresh');
    this.updateStatus(false);
    this.snackBarService.openSnackbar('Logout successfull', 'success');
  }
}
