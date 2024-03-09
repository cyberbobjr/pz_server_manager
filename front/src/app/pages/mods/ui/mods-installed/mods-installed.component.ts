import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {loadModsIni} from "@pzstore/actions/server.actions";
import {filter, map, Observable} from "rxjs";

@Component({
  selector: 'app-mods-installed',
  templateUrl: './mods-installed.component.html',
  styleUrl: './mods-installed.component.scss'
})
export class ModsInstalledComponent implements OnInit {
  mods$: Observable<any> = this.store.select((store) => store.pzStore.mods_ini)
    .pipe(
      map(r => r?.workshop_items),
      filter(r => !!r),
      map(r => r!.map(w => w.steam_data))
    );

  constructor(private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
    this.store.dispatch(loadModsIni())
  }
}
