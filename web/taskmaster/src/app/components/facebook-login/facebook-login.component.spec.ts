import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FacebookLoginComponent } from './facebook-login.component';

describe('FacebookLoginComponent', () => {
  let component: FacebookLoginComponent;
  let fixture: ComponentFixture<FacebookLoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FacebookLoginComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FacebookLoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
