import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { PaypalButtonComponent } from '../paypal-button/paypal-button.component';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-subscription-banner',
  standalone: true,
  imports: [MatToolbarModule, MatButtonModule, PaypalButtonComponent],
  templateUrl: './subscription-banner.component.html',
  styleUrl: './subscription-banner.component.scss'
})
export class SubscriptionBannerComponent {
  paypalClientId = environment.paypalClientId;
  paypalPlanId = environment.paypalPlanId;
}
