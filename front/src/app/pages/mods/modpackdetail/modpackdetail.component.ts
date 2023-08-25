import {Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Parser} from 'bulletin-board-code';
import {filter, Observable, of, switchMap, tap} from 'rxjs';
import {ModpackDetail} from '../api/Mod';
import {ModpackService} from '../service/modpack.service';
import {ModsService} from '../service/mods.service';

@Component({
  selector: 'app-modpackdetail',
  templateUrl: './modpackdetail.component.html',
  styleUrls: ['./modpackdetail.component.scss']
})
export class ModpackdetailComponent {
  modpackdetails$: Observable<ModpackDetail[]>
  parser = new Parser();
  modpackname!: string;

  constructor(private activatedRoute: ActivatedRoute,
              private modpackService: ModpackService,
              private modService: ModsService) {
    this.modpackdetails$ = this.activatedRoute
                               .paramMap
                               .pipe(
                                 filter(p => p.has('id')),
                                 tap(p => this.modpackname = p.get('id')!),
                                 switchMap(p => this.modpackService.getModpackDetails(p.get('id')!)),
                                 switchMap(m => of(
                                     m.sort((a, b) => a.mod_info.name.localeCompare(b.mod_info.name))
                                      .map(mod => ({
                                        ...mod,
                                        html_description: this.parser.toHTML(mod.steam_data!.file_description),
                                        vote: Math.round(mod.steam_data!.vote_data.score * 10)
                                      }))
                                   )
                                 ),
                                 tap(p => console.log(p))
                               )
  }
}
