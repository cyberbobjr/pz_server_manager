import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {deleteMods, loadModsIni} from "@pzstore/actions/server.actions";
import {filter, map, Observable, take} from "rxjs";
import {SteamData} from "@core/interfaces/PzModsIni";
import {MatDialog} from "@angular/material/dialog";
import {DialogDelModConfirmationComponent} from "../dialog-del-mod-confirmation/dialog-del-mod-confirmation.component";

@Component({
  selector: 'app-mods-installed',
  templateUrl: './mods-installed.component.html',
  styleUrl: './mods-installed.component.scss'
})
export class ModsInstalledComponent implements OnInit {
  mods$: Observable<any> = this.store.select((store) => store.pzStore.mods_installed)
    .pipe(
      map(r => r?.workshop_items),
      filter(r => !!r),
      map(r => r!.map(w => {
        return {...w.steam_data, Mods: w.Mods, Maps: w.Maps}
      }))
    );

  constructor(private store: Store<{ pzStore: PzStore }>,
              private dialog: MatDialog,
  ) {
  }

  ngOnInit(): void {
    this.store.dispatch(loadModsIni())
  }

  askDelete(item: SteamData) {
    const dialogRef = this.dialog.open(DialogDelModConfirmationComponent, {
      data: {mod_name: item.title},
    });
    dialogRef.afterClosed()
      .pipe(
        take(1),
        filter(r => !!r)
      )
      .subscribe(() => {
        this.store.dispatch(deleteMods({
          modsId: item.Mods!.join(";"),
          mapsId: item.Maps!.join(";"),
          workShopdId: item.publishedfileid
        }));
      });
  }
}
