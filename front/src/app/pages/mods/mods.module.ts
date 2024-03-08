import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ModsRoutingModule} from './mods-routing.module';
import {ModsIndexComponent} from "./pages/mods-index/mods-index.component";
import {ModsListComponent} from "./ui/mods-list/mods-list.component";
import {MatTabsModule} from "@angular/material/tabs";
import {MaterialModule} from "../../material.module";
import {BbodeToHtmlPipe} from "@shared/pipes/bbode-to-html.pipe";


@NgModule({
  declarations: [
    ModsIndexComponent,
    ModsListComponent
  ],
  imports: [
    CommonModule,
    ModsRoutingModule,
    MatTabsModule,
    MaterialModule,
    BbodeToHtmlPipe
  ]
})
export class ModsModule {
}
