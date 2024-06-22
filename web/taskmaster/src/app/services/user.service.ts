import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../models/user.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) {}

  getCurrentUser(): Observable<User> {
    return this.http.get<User>(environment.apiUrl + '/users/me');
  }

  deleteCurrentUser(): Observable<void> {
    return this.http.delete<void>(environment.apiUrl + '/users/me');
  }
}
