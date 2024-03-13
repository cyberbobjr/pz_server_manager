import {ComponentFixture, TestBed} from '@angular/core/testing';

import {TasksIconComponent} from './tasks-icon.component';

describe('TasksIconComponent', () => {
  let component: TasksIconComponent;
  let fixture: ComponentFixture<TasksIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TasksIconComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TasksIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
