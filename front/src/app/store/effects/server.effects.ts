import {Injectable} from "@angular/core";
import {Actions, createEffect, ofType} from "@ngrx/effects";
import {PzServerService} from "../../core/services/pz-server.service";
import {getStatus, sendCommand, serverStatusError, setCommandResult, setStatus} from "../actions/server.actions";
import {catchError, exhaustMap, map, of} from "rxjs";
import {PzStatus} from "../../core/interfaces/PzStatus";
import {PzServerReturn} from "../../core/interfaces/PzServerReturn";

@Injectable()
export class ServerEffects {
  getStatus$ = createEffect(() => this.actions$.pipe(
    ofType(getStatus),
    exhaustMap(() => this.service.getStatus()
      .pipe(
        map((result: PzStatus) => setStatus({newStatus: result})),
        catchError(error => {
          console.error(error);
          return of(serverStatusError());
        })
      ))
  ))


  sendCommand$ = createEffect(() => this.actions$.pipe(
    ofType(sendCommand),
    exhaustMap(({command}) => this.service.sendCommand(command)
      .pipe(
        map((result: PzServerReturn) => setCommandResult({result: result.msg})),
        catchError(error => {
          console.error(error);
          return of(serverStatusError());
        })
      )
    )
  ))

  constructor(
    private actions$: Actions,
    private service: PzServerService
  ) {
  }
}
