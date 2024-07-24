import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LogsIndexComponent} from "./pages/logs-index/logs-index.component";

const routes: Routes = [
  {
    path: '',
    component: LogsIndexComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LogsRoutingModule {
}
