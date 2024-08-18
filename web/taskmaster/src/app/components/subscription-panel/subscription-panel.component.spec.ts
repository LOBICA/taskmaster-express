import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubscriptionPanelComponent } from './subscription-panel.component';

describe('SubscriptionPanelComponent', () => {
  let component: SubscriptionPanelComponent;
  let fixture: ComponentFixture<SubscriptionPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubscriptionPanelComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SubscriptionPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
