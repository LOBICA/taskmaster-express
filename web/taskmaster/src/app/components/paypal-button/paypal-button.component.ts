import { Component, OnInit, Input } from '@angular/core';
import { loadScript } from '@paypal/paypal-js';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';
import { SubscriptionService } from '../../services/subscription.service';


@Component({
  selector: 'app-paypal-button',
  standalone: true,
  imports: [],
  templateUrl: './paypal-button.component.html',
  styleUrl: './paypal-button.component.scss'
})
export class PaypalButtonComponent implements OnInit {
  @Input() clientId: string = '';
  @Input() planId: string = '';
  @Input() layout: 'vertical' | 'horizontal' = 'vertical';

  user: User | undefined | null;

  constructor(
    private userService: UserService,
    private subscriptionService: SubscriptionService,
  ) {
    this.userService.getCurrentUser().subscribe(user => {
      this.user = user;
    });
  }

  ngOnInit(): void {
    const planId = this.planId;
    const userId = this.user?.uuid || undefined;

    const subscriptionService = this.subscriptionService;

    loadScript({
      "clientId": this.clientId,
      "vault": true,
      "intent": "subscription",
    }).then((paypal) => {
      if(paypal?.Buttons) {
        paypal.Buttons({
          style: {
            layout: this.layout,
          },
          createSubscription: function(data, actions) {
            return actions.subscription.create({
             'plan_id': planId,
             'custom_id': userId,
             });
           },
          onApprove: function(data, actions) {
            if (data.subscriptionID) {
              subscriptionService.linkSubscription(data.subscriptionID).subscribe(() => {
                subscriptionService.checkSubscriptionStatus();
              });
            }
            return Promise.resolve();
          },
         }).render('#paypal-button-container');
      }
    }).catch((err) => {
      console.error('failed to load the PayPal JS SDK script', err);
    });
  }
}
