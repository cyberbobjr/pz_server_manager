import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {AccordionModule} from 'primeng/accordion';
import {ButtonModule} from 'primeng/button';
import {ChipModule} from 'primeng/chip';
import {DataViewModule} from 'primeng/dataview';
import {DialogModule} from 'primeng/dialog';
import {DropdownModule} from 'primeng/dropdown';
import {InputTextModule} from 'primeng/inputtext';
import {ProgressBarModule} from 'primeng/progressbar';
import {RatingModule} from 'primeng/rating';
import {TagModule} from 'primeng/tag';
import {AppSharedModule} from '../../shared/appshared.module';
import {IndexComponent} from './pages/index/index.component';

import {ModsRoutingModule} from './mods-routing.module';
import {ModpackdetailComponent} from './pages/modpackdetail/modpackdetail.component';


@NgModule({
  declarations: [
    IndexComponent,
    ModpackdetailComponent,
  ],
  imports: [
    CommonModule,
    ModsRoutingModule,
    FormsModule,
    HttpClientModule,
    ProgressBarModule,
    DataViewModule,
    RatingModule,
    TagModule,
    ChipModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    AccordionModule,
    AppSharedModule,
    DialogModule
  ],
  providers: []
})
export class ModsModule {
}
