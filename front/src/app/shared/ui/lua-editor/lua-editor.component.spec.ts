import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LuaEditorComponent } from './lua-editor.component';

describe('LuaEditorComponent', () => {
  let component: LuaEditorComponent;
  let fixture: ComponentFixture<LuaEditorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LuaEditorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LuaEditorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
