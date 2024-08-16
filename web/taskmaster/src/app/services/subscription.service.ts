import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Subscription } from '../models/subscription.model';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  activeSubscription$ = new BehaviorSubject<boolean>(false);

  constructor(private http: HttpClient) {}

  checkSubscriptionStatus() {
    this.getSubscriptionStatus().subscribe((subscription) => {
      this.activeSubscription$.next(subscription.isActive);
    });
  }

  getSubscriptionStatus(): Observable<Subscription> {
    return this.http.get<Subscription>(`${environment.apiUrl}/subscriptions/status`);
  }

  linkSubscription(orderId: string): Observable<Subscription> {
    return this.http.post<Subscription>(`${environment.apiUrl}/subscriptions/link`, { orderId });
  }

  cancelSubscription(): Observable<Subscription> {
    return this.http.post<Subscription>(`${environment.apiUrl}/subscriptions/cancel`, {});
  }
 }
