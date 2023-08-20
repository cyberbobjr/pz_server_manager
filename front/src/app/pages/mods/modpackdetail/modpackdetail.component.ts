import {Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {map, Observable} from 'rxjs';
import {Mod} from '../api/Mod';
import {ModpackService} from '../service/modpack.service';
import {ModsService} from '../service/mods.service';

@Component({
  selector: 'app-modpackdetail',
  templateUrl: './modpackdetail.component.html',
  styleUrls: ['./modpackdetail.component.scss']
})
export class ModpackdetailComponent {

  constructor(private activatedRoute: ActivatedRoute,
              private modpackService: ModpackService,
              private modService: ModsService) {
    this.activatedRoute.paramMap.subscribe(p => {
      console.log(p.get('id'));
    });
  }
}
