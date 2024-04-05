import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {FormBuilder} from "@angular/forms";
import {getPlayers} from "@pzstore/actions/server.actions";
import {Observable} from "rxjs";

@Component({
  selector: 'app-server-players',
  templateUrl: './server-players.component.html',
  styleUrl: './server-players.component.scss'
})
export class ServerPlayersComponent implements OnInit {
  players$: Observable<string[]> = this.store.select(state => state.pzStore.players);

  constructor(private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
    this.store.dispatch(getPlayers());
  }
}
