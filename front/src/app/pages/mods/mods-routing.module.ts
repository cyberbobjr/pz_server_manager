import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {IndexComponent} from './pages/index/index.component';
import {ModpackdetailComponent} from './pages/modpackdetail/modpackdetail.component';

const routes: Routes = [
  {
    path: '',
    component: IndexComponent
  },
  {
    path: 'modpackdetail/:id',
    component: ModpackdetailComponent
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ModsRoutingModule {
}
