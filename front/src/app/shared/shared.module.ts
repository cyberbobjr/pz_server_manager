import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NotfoundComponent} from "./ui/notfound/notfound.component";
import {RouterModule} from "@angular/router";
import {ServerStatusComponent} from "./ui/server-status/server-status.component";


@NgModule({
  declarations: [
    NotfoundComponent,
  ],
  imports: [
    CommonModule,
    RouterModule,
    ServerStatusComponent
  ],
  exports: [
    ServerStatusComponent
  ]
})
export class SharedModule {
}
