import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NotfoundComponent} from "./ui/notfound/notfound.component";
import {RouterModule} from "@angular/router";
import {LuaEditorComponent} from "./ui/lua-editor/lua-editor.component";
import {FormsModule} from "@angular/forms";
import {MonacoEditorModule} from "ngx-monaco-editor-v2";
import {SpinnerComponent} from "@shared/ui/spinner/spinner.component";
import {MaterialModule} from "../material.module";
import {TasksIconComponent} from "@shared/ui/tasks-icon/tasks-icon.component";


@NgModule({
  declarations: [
    NotfoundComponent,
    LuaEditorComponent,
    SpinnerComponent,
    TasksIconComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    MonacoEditorModule,
    RouterModule,
    MaterialModule
  ],
  exports: [
    LuaEditorComponent,
    SpinnerComponent,
    TasksIconComponent
  ]
})
export class SharedModule {
}
