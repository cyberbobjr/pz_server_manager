import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {PreviewStaticPipe} from './pipe/preview-static.pipe';
import {VotePipe} from './pipe/vote.pipe';
import {StarRatingComponent} from './ui/star-rating/star-rating.component';
import { SafePipe } from './pipe/safe.pipe';


@NgModule({
  declarations: [
    VotePipe,
    PreviewStaticPipe,
    StarRatingComponent,
    SafePipe
  ],
  imports: [
    CommonModule
  ],
  exports: [
    VotePipe,
    PreviewStaticPipe,
    StarRatingComponent,
    SafePipe,
  ]
})
export class AppSharedModule {
}
