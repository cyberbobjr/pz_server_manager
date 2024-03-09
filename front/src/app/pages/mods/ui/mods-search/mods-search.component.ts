import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from "@angular/forms";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {searchMods} from "@pzstore/actions/server.actions";
import {Observable} from "rxjs";
import {WorkshopItems} from "@core/interfaces/PzModsIni";

@Component({
  selector: 'app-mods-search',
  templateUrl: './mods-search.component.html',
  styleUrl: './mods-search.component.scss'
})
export class ModsSearchComponent implements OnInit {
  mods$: Observable<WorkshopItems[]> = this.store.select((store) => store.pzStore.mods_searched);
  formSearch = this.fb.group({
    search: [null, [Validators.required]]
  })

  constructor(private fb: FormBuilder,
              private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
    this.store.dispatch(searchMods({cursor: undefined, text: undefined}));
  }

}
