import {CommonModule} from '@angular/common';
import {HttpClientModule} from '@angular/common/http';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {AccordionModule} from 'primeng/accordion';
import {ButtonModule} from 'primeng/button';
import {ChipModule} from 'primeng/chip';
import {DataViewModule} from 'primeng/dataview';
import {DropdownModule} from 'primeng/dropdown';
import {InputTextModule} from 'primeng/inputtext';
import {ProgressBarModule} from 'primeng/progressbar';
import {RatingModule} from 'primeng/rating';
import {TagModule} from 'primeng/tag';
import {IndexComponent} from './index/index.component';

import {ModsRoutingModule} from './mods-routing.module';
import {VotePipe} from './pipe/vote.pipe';
import {ModpackService} from './service/modpack.service';
import {StarRatingComponent} from './ui/star-rating/star-rating.component';
import { ModpackdetailComponent } from './modpackdetail/modpackdetail.component';
import { PreviewStaticPipe } from './pipe/preview-static.pipe';


@NgModule({
  declarations: [
    IndexComponent,
    VotePipe,
    StarRatingComponent,
    ModpackdetailComponent,
    PreviewStaticPipe
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
    AccordionModule
  ],
  providers: [

  ]
})
export class ModsModule {
}
