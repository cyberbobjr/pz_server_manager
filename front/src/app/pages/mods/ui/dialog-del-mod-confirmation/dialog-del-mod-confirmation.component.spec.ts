import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogDelModConfirmationComponent } from './dialog-del-mod-confirmation.component';

describe('DialogDelModConfirmationComponent', () => {
  let component: DialogDelModConfirmationComponent;
  let fixture: ComponentFixture<DialogDelModConfirmationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DialogDelModConfirmationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DialogDelModConfirmationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
