import { Component, OnInit, Input, input } from '@angular/core';
import { loadScript } from '@paypal/paypal-js';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';


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
  ) {
    this.userService.getCurrentUser().subscribe(user => {
      this.user = user;
    });
  }

  ngOnInit(): void {
    const planId = this.planId;
    const userId = this.user?.uuid || undefined;

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
         }).render('#paypal-button-container');
      }
    }).catch((err) => {
      console.error('failed to load the PayPal JS SDK script', err);
    });
  }
}
