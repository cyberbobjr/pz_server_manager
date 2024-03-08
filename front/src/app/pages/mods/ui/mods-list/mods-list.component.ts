import {Component, OnInit} from '@angular/core';
import {map, Observable} from "rxjs";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {loadModsIni} from "@pzstore/actions/server.actions";

@Component({
  selector: 'app-mods-list',
  templateUrl: './mods-list.component.html',
  styleUrl: './mods-list.component.scss'
})
export class ModsListComponent implements OnInit {
  mods$: Observable<any> = this.store.select((store) => store.pzStore.mods_ini)
    .pipe(
      map(r => r?.workshop_items)
    );
  columnsToDisplay = [
    "WorkshopItems",
    "Mods",
    "preview_url",
    "file_description"
  ];
  expandedStates: { [key: string]: boolean } = {}; // Utilisation d'un objet pour stocker l'état d'expansion par ligne

  constructor(private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
    this.store.dispatch(loadModsIni())
  }

  toggleDescription(rowId: string) {
    this.expandedStates[rowId] = !this.expandedStates[rowId];
  }

  isExpanded(rowId: string): boolean {
    return this.expandedStates[rowId];
  }
}
