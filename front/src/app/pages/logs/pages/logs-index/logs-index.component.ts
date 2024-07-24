import {Component, OnInit} from '@angular/core';
import {filter, map, Observable, startWith, switchMap} from "rxjs";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {loadLogPlayers, searchLogs} from "@pzstore/actions/server.actions";
import {FormBuilder, FormControl} from "@angular/forms";

@Component({
  selector: 'app-logs-index',
  templateUrl: './logs-index.component.html',
  styleUrl: './logs-index.component.scss'
})
export class LogsIndexComponent implements OnInit {
  players$: Observable<string[]> = this.store.select(state => state.pzStore.players);
  logs$ = this.store.select(state => state.pzStore.logs);
  loading$ = this.store.select(state => state.pzStore.loading);
  error$ = this.store.select(state => state.pzStore.error);
  playerControl = new FormControl(null);
  filteredplayers$: Observable<string[]> = new Observable<string[]>();
  searchForm = this.fb.group({
    player: [null],
    startDate: [null],
    endDate: [null],
    logType: [null],
  })
  player?: string;
  startDate?: string;
  endDate?: string;
  logType?: string;
  logTypes: string[] = ['ITEMS', 'MAPS', 'ACTIONS', 'PERKS'];

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }


  ngOnInit(): void {
    this.filteredplayers$ = this.searchForm.get('player')!.valueChanges.pipe(
      startWith(''),
      switchMap(value => this._filter(value || '')),
    );
    this.refresh();
  }

  private _filter(value: string): Observable<string[]> {
    const filterValue = value.toLowerCase();

    return this.players$.pipe(
      map(p => p.filter(player => player.toLowerCase().includes(filterValue)))
    )
  }

  refresh() {
    this.store.dispatch(loadLogPlayers())
  }

  searchLogs() {
    this.store.dispatch(searchLogs({
      player: this.searchForm.value.player!,
      startDate: this.searchForm.value.startDate!,
      endDate: this.searchForm.value.endDate!,
      logType: this.searchForm.value.logType!
    }));
  }
}
