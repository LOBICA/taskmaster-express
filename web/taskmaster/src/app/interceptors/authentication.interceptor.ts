import { HttpErrorResponse, HttpEvent, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { Inject } from '@angular/core';
import { Observable, catchError, throwError } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt';
import { LoginService } from '../services/login.service';

export const authenticationInterceptor: HttpInterceptorFn = (req, next) => {
  const url = req.url;
  if (!url.includes('token')) {
    return retrieveToken(req, next).pipe(
      catchError((error) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          return handleSessionExpiredError(req, next);
        }
        return throwError(() => error);
      })
    );
  }
  return next(req);
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function handleSessionExpiredError(request: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const loginService: LoginService = Inject(LoginService);
  localStorage.removeItem('jwt');
  loginService.updateStatus(false);
  return next(request);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function retrieveToken(request: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const token = localStorage.getItem('jwt');
  const jwtHelper = new JwtHelperService();
  const tokenExpired = jwtHelper.isTokenExpired(token);
  if (token) {
    if (tokenExpired) {
      return handleSessionExpiredError(request, next);
    }
    return next(appendAccessToken(request));
  } else {
    return next(request);
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function appendAccessToken(request: HttpRequest<any>): HttpRequest<any> {
  const token = localStorage.getItem('jwt');
  return request.clone({
    headers: request.headers.set('Authorization', `Bearer ${token}`),
  });
}
