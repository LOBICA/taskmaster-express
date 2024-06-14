import { HttpErrorResponse, HttpEvent, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { Observable, catchError, filter, switchMap, take, throwError } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt';
import { LoginService } from '../services/login.service';

export const authenticationInterceptor: HttpInterceptorFn = (req, next) => {
  const url = req.url;
  const loginService: LoginService = inject(LoginService);
  if (!url.includes('token') && !url.includes('refresh')) {
    return retrieveToken(req, next).pipe(
      catchError((error) => {
        if (error instanceof HttpErrorResponse && error.status === 401) {
          return handleSessionExpiredError(req, next, loginService);
        }
        return throwError(() => error);
      })
    );
  }
  return next(req);
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function handleSessionExpiredError(request: HttpRequest<any>, next: HttpHandlerFn, loginService: LoginService): Observable<HttpEvent<unknown>> {
  loginService.logout();
  return next(request);
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function retrieveToken(request: HttpRequest<any>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const token = localStorage.getItem('jwt');
  const refresh = localStorage.getItem('refresh');
  const jwtHelper = new JwtHelperService();
  const loginService = inject(LoginService)
  const tokenExpired = jwtHelper.isTokenExpired(token);
  if (token && refresh) {
    if (tokenExpired) {
      if (!loginService.tokenRefreshing) {
        loginService.tokenRefreshing = true;
        loginService.refreshedToken$.next(null);
        return loginService.getRefreshedToken(refresh).pipe(switchMap((credentails) => {
          loginService.tokenRefreshing = false;
          localStorage.setItem('jwt', credentails.access_token);
          localStorage.setItem('refresh', credentails.refresh_token);
          loginService.refreshedToken$.next(credentails.access_token);
          return next(appendAccessToken(request));
        }))
      } else {
        return loginService.refreshedToken$.pipe(
          filter((token) => token !== null),
          take(1),
          switchMap(() => next(appendAccessToken(request)))
        )
      }
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
