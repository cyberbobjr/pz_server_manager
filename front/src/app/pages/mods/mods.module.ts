import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {ModsRoutingModule} from './mods-routing.module';
import {ModsIndexComponent} from "./pages/mods-index/mods-index.component";
import {ModsListComponent} from "./ui/mods-list/mods-list.component";
import {MatTabsModule} from "@angular/material/tabs";
import {MaterialModule} from "../../material.module";
import {BbcodeToHtmlPipe} from "@shared/pipes/bbode-to-html.pipe";
import {ModsSearchComponent} from "./ui/mods-search/mods-search.component";
import {ReactiveFormsModule} from "@angular/forms";
import {ModsInstalledComponent} from "./ui/mods-installed/mods-installed.component";
import {SharedModule} from "@shared/shared.module";
import {TablerIconsModule} from "angular-tabler-icons";

@NgModule({
  declarations: [
    ModsIndexComponent,
    ModsListComponent,
    ModsSearchComponent,
    ModsInstalledComponent
  ],
    imports: [
        CommonModule,
        ModsRoutingModule,
        MatTabsModule,
        MaterialModule,
        BbcodeToHtmlPipe,
        ReactiveFormsModule,
        SharedModule,
        TablerIconsModule
    ]
})
export class ModsModule {
}
