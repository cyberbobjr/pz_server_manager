import {RouterModule} from '@angular/router';
import {NgModule} from '@angular/core';
import {AppLayoutComponent} from "./layout/app.layout.component";
import {NotfoundComponent} from "./shared/ui/notfound/notfound.component";

@NgModule({
  imports: [
    RouterModule.forRoot([
      {
        path: '', component: AppLayoutComponent,
        children: [
          {
            path: '',
            loadChildren: () => import('./pages/dashboard/dashboard.module').then(m => m.DashboardModule)
          },
          {
            path: 'mods',
            loadChildren: () => import('./pages/mods/mods.module').then(m => m.ModsModule)
          }
        ]
      },
      {path: 'auth', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule)},
      {path: 'notfound', component: NotfoundComponent},
      {path: '**', redirectTo: '/notfound'},
    ], {scrollPositionRestoration: 'enabled', anchorScrolling: 'enabled', onSameUrlNavigation: 'reload'})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
