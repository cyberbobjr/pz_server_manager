import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {NotfoundComponent} from "./ui/notfound/notfound.component";
import {RouterModule} from "@angular/router";


@NgModule({
  declarations: [
    NotfoundComponent,
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class SharedModule {
}
