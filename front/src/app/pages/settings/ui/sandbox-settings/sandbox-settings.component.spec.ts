import {ComponentFixture, TestBed} from '@angular/core/testing';

import {SandboxSettingsComponent} from './sandbox-settings.component';

describe('SandboxSettingsComponent', () => {
  let component: SandboxSettingsComponent;
  let fixture: ComponentFixture<SandboxSettingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SandboxSettingsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SandboxSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
