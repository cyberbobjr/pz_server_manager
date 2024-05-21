import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SourceDisplayComponent } from './source-display.component';

describe('SourceDisplayComponent', () => {
  let component: SourceDisplayComponent;
  let fixture: ComponentFixture<SourceDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SourceDisplayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SourceDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
