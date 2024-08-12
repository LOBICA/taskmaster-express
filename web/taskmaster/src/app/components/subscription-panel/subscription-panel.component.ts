import { Component } from '@angular/core';
import { PaypalButtonComponent } from '../paypal-button/paypal-button.component';

@Component({
  selector: 'app-subscription-panel',
  standalone: true,
  imports: [PaypalButtonComponent],
  templateUrl: './subscription-panel.component.html',
  styleUrl: './subscription-panel.component.scss'
})
export class SubscriptionPanelComponent {

}
