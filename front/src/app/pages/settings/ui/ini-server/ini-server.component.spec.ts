import {ComponentFixture, TestBed} from '@angular/core/testing';

import {IniServerComponent} from './ini-server.component';

describe('IniServerComponent', () => {
  let component: IniServerComponent;
  let fixture: ComponentFixture<IniServerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [IniServerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IniServerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
