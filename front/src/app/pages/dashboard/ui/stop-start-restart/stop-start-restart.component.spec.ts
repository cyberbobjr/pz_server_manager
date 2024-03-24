import {ComponentFixture, TestBed} from '@angular/core/testing';

import {StopStartRestartComponent} from './stop-start-restart.component';

describe('StopStartRestartComponent', () => {
  let component: StopStartRestartComponent;
  let fixture: ComponentFixture<StopStartRestartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StopStartRestartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StopStartRestartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
