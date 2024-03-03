import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ModsRoutingModule} from './mods-routing.module';
import {ModsIndexComponent} from "./pages/mods-index/mods-index.component";


@NgModule({
  declarations: [
    ModsIndexComponent
  ],
  imports: [
    CommonModule,
    ModsRoutingModule
  ]
})
export class ModsModule {
}
