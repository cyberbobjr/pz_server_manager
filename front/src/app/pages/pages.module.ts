import {NgModule} from '@angular/core';
import {RouterModule} from '@angular/router';
import {CommonModule} from '@angular/common';
import {PagesRoutes} from './pages.routing.module';
import {MaterialModule} from '../material.module';
import {FormsModule} from '@angular/forms';
import {NgApexchartsModule} from 'ng-apexcharts';
// icons
import {TablerIconsModule} from 'angular-tabler-icons';
import * as TablerIcons from 'angular-tabler-icons/icons';
import {AppDashboardComponent} from './dashboard/dashboard.component';
import {SharedModule} from "../shared/shared.module";
import {ServerSendCommandComponent} from "../shared/ui/server-send-command/server-send-command.component";

@NgModule({
  declarations: [AppDashboardComponent],
  imports: [
    CommonModule,
    MaterialModule,
    FormsModule,
    NgApexchartsModule,
    RouterModule.forChild(PagesRoutes),
    TablerIconsModule.pick(TablerIcons),
    SharedModule,
    ServerSendCommandComponent
  ],
  exports: [TablerIconsModule],
})
export class PagesModule {
}
