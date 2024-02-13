import {HashLocationStrategy, LocationStrategy} from '@angular/common';
import {NgModule} from '@angular/core';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {AppLayoutModule} from './layout/app.layout.module';
import {ModpackService} from './pages/mods/service/modpack.service';
import {HTTP_INTERCEPTORS} from "@angular/common/http";
import {SharedModule} from "./shared/shared.module";
import {JwtInterceptor} from "./auth/services/jwt-interceptor.service";
import {AuthInterceptor} from "./auth/services/auth-interceptor.service";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    AppRoutingModule,
    AppLayoutModule,
    SharedModule
  ],
  providers: [
    {provide: LocationStrategy, useClass: HashLocationStrategy},
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true},
    ModpackService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
