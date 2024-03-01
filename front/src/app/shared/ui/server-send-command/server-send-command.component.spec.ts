import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServerSendCommandComponent } from './server-send-command.component';

describe('ServerSendCommandComponent', () => {
  let component: ServerSendCommandComponent;
  let fixture: ComponentFixture<ServerSendCommandComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServerSendCommandComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ServerSendCommandComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
