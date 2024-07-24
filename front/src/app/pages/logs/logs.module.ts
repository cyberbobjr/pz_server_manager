import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';

import {LogsRoutingModule} from './logs-routing.module';
import {LogsIndexComponent} from "./pages/logs-index/logs-index.component";
import {MaterialModule} from "@app-material/material.module";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatDatetimepickerModule, MatNativeDatetimeModule} from "@mat-datetimepicker/core";
import {MAT_DATE_LOCALE, NativeDateAdapter} from "@angular/material/core";


@NgModule({
  declarations: [
    LogsIndexComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    LogsRoutingModule,
    MaterialModule,
    FormsModule,
    MatNativeDatetimeModule,
    MatDatetimepickerModule
  ],
  providers: [
    NativeDateAdapter
  ]
})
export class LogsModule {
}
