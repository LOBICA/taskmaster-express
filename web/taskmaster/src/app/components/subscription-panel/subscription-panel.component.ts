import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog } from '@angular/material/dialog';
import { environment } from '../../../environments/environment';
import { PaypalButtonComponent } from '../paypal-button/paypal-button.component';
import { ConfirmDialogComponent } from '../confirm-dialog/confirm-dialog.component';
import { SubscriptionService } from '../../services/subscription.service';


@Component({
  selector: 'app-subscription-panel',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, PaypalButtonComponent],
  templateUrl: './subscription-panel.component.html',
  styleUrl: './subscription-panel.component.scss'
})
export class SubscriptionPanelComponent implements OnInit, OnDestroy {
  paypalClientId = environment.paypalClientId;
  paypalPlanId = environment.paypalPlanId;

  subscriptionStatus: boolean = false;
  unsubscribe$ = new Subject<void>();

  constructor(private subscriptionService: SubscriptionService, private dialog: MatDialog) {}

  ngOnInit(): void {
    this.subscriptionService.activeSubscription$.pipe(takeUntil(this.unsubscribe$)).subscribe((status) => {
      console.log('Subscription status:', status);
      this.subscriptionStatus = status;
    });
    this.subscriptionService.checkSubscriptionStatus();
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  cancelSubscription(): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Cancel Subscription',
        description: 'Do you want to cancel your current subscription?',
        buttons: {
          cancelTitle: 'No',
          confirmTitle: 'Yes'
        },
        buttonColor: 'warn'
      }
    });

    dialogRef.afterClosed().subscribe((confirm) => {
      if (confirm) {
        this.subscriptionService.cancelSubscription().subscribe(() => {
          this.subscriptionService.checkSubscriptionStatus();
        });
      }
    });
  }
}
