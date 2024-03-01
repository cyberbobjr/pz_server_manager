import {Component} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {Observable} from "rxjs";
import {PzStatus} from "../../../core/interfaces/PzStatus";
import {CommonModule} from "@angular/common";
import {MaterialModule} from "../../../material.module";
import {sendServerAction} from "../../../store/actions/server.actions";
import {PzServerAction} from "../../../core/interfaces/PzServerAction";

@Component({
  selector: 'app-stop-start-restart',
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule
  ],
  templateUrl: './stop-start-restart.component.html',
  styleUrl: './stop-start-restart.component.scss'
})
export class StopStartRestartComponent {
  status$: Observable<PzStatus | null> = this.store.select(store => store.pzStore.status);

  constructor(private store: Store<{ pzStore: PzStore }>) {
  }

  forceStop() {
    this.store.dispatch(sendServerAction({action: PzServerAction.FORCESTOP}));
  }

  stop() {
    this.store.dispatch(sendServerAction({action: PzServerAction.STOP}));
  }

  start() {
    this.store.dispatch(sendServerAction({action: PzServerAction.START}));
  }

  restart() {
    this.store.dispatch(sendServerAction({action: PzServerAction.RESTART}));
  }

}
