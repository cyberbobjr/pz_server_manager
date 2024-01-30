import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from 'primeng/api';
import {ButtonModule} from 'primeng/button';
import {ChipModule} from 'primeng/chip';
import {DataViewModule} from 'primeng/dataview';
import {DropdownModule} from 'primeng/dropdown';
import {InputTextModule} from 'primeng/inputtext';
import {ProgressBarModule} from 'primeng/progressbar';
import {AppSharedModule} from '../../shared/appshared.module';

import { SteamRoutingModule } from './steam-routing.module';
import { IndexComponent } from './pages/index/index.component';


@NgModule({
  declarations: [
    IndexComponent
  ],
  imports: [
    CommonModule,
    SteamRoutingModule,
    ButtonModule,
    ChipModule,
    DataViewModule,
    DropdownModule,
    InputTextModule,
    SharedModule,
    ProgressBarModule,
    AppSharedModule,
    ReactiveFormsModule
  ]
})
export class SteamModule { }
