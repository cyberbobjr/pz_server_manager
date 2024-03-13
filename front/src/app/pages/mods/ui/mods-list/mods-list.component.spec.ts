import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ModsListComponent} from './mods-list.component';

describe('ModsListComponent', () => {
  let component: ModsListComponent;
  let fixture: ComponentFixture<ModsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModsListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
