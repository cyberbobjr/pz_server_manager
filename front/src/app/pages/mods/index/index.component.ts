import {Component, ViewChild} from '@angular/core';
import {DataView} from 'primeng/dataview';
import {BehaviorSubject, firstValueFrom, Observable} from 'rxjs';
import {Mod} from '../api/Mod';
import {ModpackService} from '../service/modpack.service';
import {ModsService} from '../service/mods.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent {
  @ViewChild('dv', {static: false}) dv!: DataView;
  modpacks$: BehaviorSubject<string[]> = this.modpackService.modpacks$;
  mods$: Observable<Mod[]> = this.modsService.mods$;
  selectedModpack!: string;

  constructor(private modsService: ModsService,
              private modpackService: ModpackService) {
  }

  Myfilter(filter: string, filterMatchMode: string = "contains") {
    this.dv.filter(filter, filterMatchMode);
  }

  addToModpack(product: Mod) {
    firstValueFrom(this.modpackService.addModIdToModpack(this.selectedModpack, product.mod_info.dir));
  }
}
