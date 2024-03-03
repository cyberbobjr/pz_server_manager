import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ModsIndexComponent} from "./pages/mods-index/mods-index.component";

const routes: Routes = [
  {
    path: '',
    component: ModsIndexComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ModsRoutingModule {
}
