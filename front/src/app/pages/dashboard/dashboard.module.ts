import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {DashboardRoutingModule} from './dashboard-routing.module';
import {AppDashboardComponent} from "./pages/dashboard/dashboard.component";
import {MaterialModule} from "@app-material/material.module";
import {ServerStatusComponent} from "./ui/server-status/server-status.component";
import {ServerSendCommandComponent} from "./ui/server-send-command/server-send-command.component";
import {StopStartRestartComponent} from "./ui/stop-start-restart/stop-start-restart.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RunningTimePipe} from "./pipes/running-time.pipe";


@NgModule({
  declarations: [
    AppDashboardComponent,
    ServerSendCommandComponent,
    StopStartRestartComponent,
    ServerStatusComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    DashboardRoutingModule,
    MaterialModule,
    RunningTimePipe
  ]
})
export class DashboardModule {
}
