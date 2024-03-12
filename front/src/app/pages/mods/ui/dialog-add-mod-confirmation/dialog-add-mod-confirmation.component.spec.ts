import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogAddModConfirmationComponent } from './dialog-add-mod-confirmation.component';

describe('DialogAddModConfirmationComponent', () => {
  let component: DialogAddModConfirmationComponent;
  let fixture: ComponentFixture<DialogAddModConfirmationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DialogAddModConfirmationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DialogAddModConfirmationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
