import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModsInstalledComponent } from './mods-installed.component';

describe('ModsInstalledComponent', () => {
  let component: ModsInstalledComponent;
  let fixture: ComponentFixture<ModsInstalledComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModsInstalledComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ModsInstalledComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
