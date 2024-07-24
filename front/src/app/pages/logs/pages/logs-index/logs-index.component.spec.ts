import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogsIndexComponent } from './logs-index.component';

describe('LogsIndexComponent', () => {
  let component: LogsIndexComponent;
  let fixture: ComponentFixture<LogsIndexComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LogsIndexComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LogsIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
