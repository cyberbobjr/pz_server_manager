import {Component} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Observable} from 'rxjs';
import {Mod} from '../../../mods/api/Mod';
import {SteamService} from '../../services/steam.service';

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent {
  latestMods$: Observable<Mod[]> = this.steamService.getLatestMods();
  searchForm: FormGroup = this.fb.group({
    name: [null, [Validators.required]]
  })

  constructor(private steamService: SteamService, private fb: FormBuilder) {
  }

  search() {
    this.latestMods$ = this.steamService.searchMods(this.searchForm.get('name')?.value);
  }
}
