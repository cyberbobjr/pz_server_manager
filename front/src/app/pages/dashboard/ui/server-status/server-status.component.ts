import {Component, OnDestroy, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {PzStatus} from "@core/interfaces/PzStatus";
import {interval, Observable, Subscription} from "rxjs";
import {getPlayersCount} from "@pzstore/actions/server.actions";

@Component({
  selector: 'app-server-status',
  templateUrl: './server-status.component.html',
  styleUrl: './server-status.component.scss'
})
export class ServerStatusComponent implements OnInit, OnDestroy {
  status$: Observable<PzStatus | null>;
  playerCount$: Observable<number>;
  isServerMonitored$: Observable<boolean | undefined> = this.store.select((store) => store.pzStore.serverConfig?.pz.monitoring);
  private subscription: Subscription = new Subscription();

  constructor(private store: Store<{ pzStore: PzStore }>) {
    this.status$ = this.store.select(store => store.pzStore.status);
    this.playerCount$ = this.store.select(store => store.pzStore.playerCount);
    this.store.dispatch(getPlayersCount());
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  ngOnInit(): void {
    this.subscription.add(
      interval(30000).subscribe(_ => this.store.dispatch(getPlayersCount()))
    )
  }
}
