import { Component, OnInit, Input } from '@angular/core';
import { loadScript } from '@paypal/paypal-js';


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

  constructor() { }

  ngOnInit(): void {
    const planId = this.planId;

    loadScript({
      "clientId": this.clientId,
      "vault": true,
      "intent": "subscription",
    }).then((paypal) => {
      if(paypal?.Buttons) {
        paypal.Buttons({
          createSubscription: function(data, actions) {
            return actions.subscription.create({
             'plan_id': planId,
             });
           },
         }).render('#paypal-button-container');
      }
    }).catch((err) => {
      console.error('failed to load the PayPal JS SDK script', err);
    });
  }
}
