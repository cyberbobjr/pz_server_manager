import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NotfoundComponent} from "./ui/notfound/notfound.component";
import {RouterModule} from "@angular/router";
import {ServerStatusComponent} from "./ui/server-status/server-status.component";
import {LuaEditorComponent} from "./ui/lua-editor/lua-editor.component";
import {FormsModule} from "@angular/forms";
import {MonacoEditorModule} from "ngx-monaco-editor-v2";


@NgModule({
  declarations: [
    NotfoundComponent,
    LuaEditorComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    MonacoEditorModule,
    RouterModule,
    ServerStatusComponent
  ],
  exports: [
    ServerStatusComponent,
    LuaEditorComponent
  ]
})
export class SharedModule {
}
