import {HashLocationStrategy, LocationStrategy} from '@angular/common';
import {NgModule} from '@angular/core';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {NotfoundComponent} from './demo/components/notfound/notfound.component';
import {AppLayoutModule} from './layout/app.layout.module';
import {ModpackService} from './pages/mods/service/modpack.service';

@NgModule({
  declarations: [
    AppComponent,
    NotfoundComponent
  ],
  imports: [
    AppRoutingModule,
    AppLayoutModule
  ],
  providers: [
    {provide: LocationStrategy, useClass: HashLocationStrategy},
    ModpackService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
