import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ModsIndexComponent} from './mods-index.component';

describe('ModsIndexComponent', () => {
  let component: ModsIndexComponent;
  let fixture: ComponentFixture<ModsIndexComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModsIndexComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModsIndexComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
