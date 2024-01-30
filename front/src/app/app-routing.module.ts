import {RouterModule} from '@angular/router';
import {NgModule} from '@angular/core';
import {NotfoundComponent} from './demo/components/notfound/notfound.component';
import {AppLayoutComponent} from "./layout/app.layout.component";

@NgModule({
  imports: [
    RouterModule.forRoot([
      {
        path: '', component: AppLayoutComponent,
        children: [
          {
            path: '',
            loadChildren: () => import('./demo/components/dashboard/dashboard.module').then(m => m.DashboardModule)
          },
          {
            path: 'mods',
            loadChildren: () => import('./pages/mods/mods.module').then(m => m.ModsModule)
          },
          {
            path: 'steam',
            loadChildren: () => import('./pages/steam/steam.module').then(m => m.SteamModule)
          }
        ]
      },
      {path: 'auth', loadChildren: () => import('./demo/components/auth/auth.module').then(m => m.AuthModule)},
      {path: 'notfound', component: NotfoundComponent},
      {path: '**', redirectTo: '/notfound'},
    ], {scrollPositionRestoration: 'enabled', anchorScrolling: 'enabled', onSameUrlNavigation: 'reload'})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
