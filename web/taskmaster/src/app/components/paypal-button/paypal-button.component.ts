import { Component, OnInit } from '@angular/core';
import { loadScript } from '@paypal/paypal-js';
import { environment } from '../../../environments/environment';


@Component({
  selector: 'app-paypal-button',
  standalone: true,
  imports: [],
  templateUrl: './paypal-button.component.html',
  styleUrl: './paypal-button.component.scss'
})
export class PaypalButtonComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    loadScript({ "clientId": environment.paypalClientId, "vault": true, "intent": "subscription" }).then((paypal) => {
      if(paypal?.Buttons) {
        paypal.Buttons({
          createSubscription: function(data, actions) {
            return actions.subscription.create({
             'plan_id': environment.paypalPlanId,
             });
           },
         }).render('#paypal-button-container');
      }
    }).catch((err) => {
      console.error('failed to load the PayPal JS SDK script', err);
    });
  }
}
