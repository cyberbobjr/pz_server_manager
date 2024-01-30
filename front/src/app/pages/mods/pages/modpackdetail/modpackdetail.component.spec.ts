import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModpackdetailComponent } from './modpackdetail.component';

describe('ModpackdetailComponent', () => {
  let component: ModpackdetailComponent;
  let fixture: ComponentFixture<ModpackdetailComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModpackdetailComponent]
    });
    fixture = TestBed.createComponent(ModpackdetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
