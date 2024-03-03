import {CommonModule, HashLocationStrategy, LocationStrategy} from '@angular/common';
import {NgModule, isDevMode} from '@angular/core';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {SharedModule} from "./shared/shared.module";
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AuthInterceptor} from "./core/services/auth-interceptor.service";
import {JwtInterceptor} from "./core/services/jwt-interceptor.service";
import {FullComponent} from "./layouts/full/full.component";
import {BlankComponent} from "./layouts/blank/blank.component";
import {MaterialModule} from "./material.module";
import {SidebarComponent} from "./layouts/full/sidebar/sidebar.component";
import {BrandingComponent} from "./layouts/full/sidebar/branding.component";
import {AppNavItemComponent} from "./layouts/full/sidebar/nav-item/nav-item.component";
import {HeaderComponent} from "./layouts/full/header/header.component";
import {TablerIconsModule} from "angular-tabler-icons";
import * as TablerIcons from 'angular-tabler-icons/icons';
import {StoreModule} from '@ngrx/store';
import {pzReducer} from "./store/reducers/server.reducer";
import {StoreDevtoolsModule} from '@ngrx/store-devtools';
import {EffectsModule} from '@ngrx/effects';
import {ServerEffects} from "./store/effects/server.effects";
import {MonacoEditorModule} from "ngx-monaco-editor-v2";

@NgModule({
  declarations: [
    AppComponent,
    FullComponent,
    BlankComponent,
    SidebarComponent,
    BrandingComponent,
    AppNavItemComponent,
    HeaderComponent
  ],
  imports: [
    AppRoutingModule,
    SharedModule,
    CommonModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    MonacoEditorModule.forRoot(),
    TablerIconsModule.pick(TablerIcons),
    StoreModule.forRoot({pzStore: pzReducer}, {}),
    StoreDevtoolsModule.instrument({maxAge: 25, logOnly: !isDevMode()}),
    EffectsModule.forRoot([ServerEffects]),
  ],
  providers: [
    {provide: LocationStrategy, useClass: HashLocationStrategy},
    {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
