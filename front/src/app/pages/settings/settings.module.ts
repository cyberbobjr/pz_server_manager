import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {SettingsRoutingModule} from './settings-routing.module';
import {IniServerComponent} from "./ui/ini-server/ini-server.component";
import {IndexComponent} from "./pages/index/index.component";
import {SharedModule} from "@shared/shared.module";
import {MaterialModule} from "../../material.module";
import {SandboxSettingsComponent} from "./ui/sandbox-settings/sandbox-settings.component";
import {ReactiveFormsModule} from "@angular/forms";
import {ManagerSettingsComponent} from "./ui/manager-settings/manager-settings.component";


@NgModule({
  declarations: [
    IniServerComponent,
    IndexComponent,
    ManagerSettingsComponent,
    SandboxSettingsComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule,
    MaterialModule,
    SettingsRoutingModule
  ]
})
export class SettingsModule {
}
