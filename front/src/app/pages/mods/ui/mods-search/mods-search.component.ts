import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from "@angular/forms";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {addMods, saveMods, searchMods} from "@pzstore/actions/server.actions";
import {filter, Observable, take} from "rxjs";
import {SteamData, WorkshopItems} from "@core/interfaces/PzModsIni";
import {ExtractModInfosPipe} from "@shared/pipes/extract-mod-infos.pipe";
import {MatDialog} from "@angular/material/dialog";
import {DialogAddModConfirmationComponent} from "../dialog-add-mod-confirmation/dialog-add-mod-confirmation.component";

@Component({
  selector: 'app-mods-search',
  templateUrl: './mods-search.component.html',
  styleUrl: './mods-search.component.scss',
  providers: [
    ExtractModInfosPipe
  ]
})
export class ModsSearchComponent implements OnInit {
  loading$: Observable<boolean> = this.store.select((store) => store.pzStore.loading);
  mods$: Observable<WorkshopItems[]> = this.store.select((store) => store.pzStore.mods_searched);
  formSearch = this.fb.group({
    search: [null, [Validators.required]]
  })

  constructor(private fb: FormBuilder,
              private extractModInfosPipe: ExtractModInfosPipe,
              private dialog: MatDialog,
              private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
    this.store.dispatch(searchMods({cursor: undefined, text: undefined}));
  }

  addMod(item: SteamData) {
    const {modIds, mapFolders} = this.extractModInfosPipe.transform(item.file_description);
    const dialogRef = this.dialog.open(DialogAddModConfirmationComponent, {
      data: {mods: modIds.join(";"), workshop: item.publishedfileid, maps: mapFolders.join(";")},
    });

    dialogRef.afterClosed()
      .pipe(
        take(1),
        filter(r => !!r && !!r.workshop)
      )
      .subscribe((result: { mods: string, workshop: string, maps: string }) => {
        if (result.mods.length === 0 && result.maps.length === 0) {
          return
        }
        this.store.dispatch(addMods({workShopdId: result.workshop, modsId: result.mods, mapsId: result.maps}))
        this.store.dispatch(saveMods());
      });
  }
}
