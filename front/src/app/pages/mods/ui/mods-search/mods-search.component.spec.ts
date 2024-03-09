import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModsSearchComponent } from './mods-search.component';

describe('ModsSearchComponent', () => {
  let component: ModsSearchComponent;
  let fixture: ComponentFixture<ModsSearchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModsSearchComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModsSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
