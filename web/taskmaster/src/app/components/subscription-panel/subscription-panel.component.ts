import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { PaypalButtonComponent } from '../paypal-button/paypal-button.component';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-subscription-panel',
  standalone: true,
  imports: [MatCardModule, PaypalButtonComponent],
  templateUrl: './subscription-panel.component.html',
  styleUrl: './subscription-panel.component.scss'
})
export class SubscriptionPanelComponent {
  paypalClientId = environment.paypalClientId;
  paypalPlanId = environment.paypalPlanId;
}
