import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-subscription-banner',
  standalone: true,
  imports: [MatToolbarModule, MatButtonModule],
  templateUrl: './subscription-banner.component.html',
  styleUrl: './subscription-banner.component.scss'
})
export class SubscriptionBannerComponent {}
