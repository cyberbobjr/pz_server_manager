import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ServerPlayersComponent } from './server-players.component';

describe('ServerPlayersComponent', () => {
  let component: ServerPlayersComponent;
  let fixture: ComponentFixture<ServerPlayersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServerPlayersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ServerPlayersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
