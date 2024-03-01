import {Injectable} from "@angular/core";
import {Actions, createEffect, ofType} from "@ngrx/effects";
import {PzServerService} from "../../core/services/pz-server.service";
import {
  sendServerAction,
  getIniConfig,
  getPlayersCount,
  getStatus,
  sendCommand,
  serverStatusError,
  setCommandResult,
  setIniConfig,
  setPlayersCount,
  setStatus
} from "../actions/server.actions";
import {catchError, exhaustMap, filter, map, of} from "rxjs";
import {PzStatus} from "../../core/interfaces/PzStatus";
import {PzServerReturn} from "../../core/interfaces/PzServerReturn";
import {PzServerAction} from "../../core/interfaces/PzServerAction";

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

  getPlayerCount$ = createEffect(() => this.actions$.pipe(
    ofType(getPlayersCount),
    exhaustMap(() => this.service.sendCommand('players').pipe(
      map(result => {
        const regex = /\((\d+)\)/;
        const match = regex.exec(result.msg);
        let playerCount = 0;
        if (match && match.length > 1) {
          playerCount = +match[1];
        }
        return setPlayersCount({count: playerCount})
      }),
      catchError(error => {
        console.error(error);
        return of(serverStatusError());
      })
    ))
  ))

  getIniConfig = createEffect(() => this.actions$.pipe(
    ofType(getIniConfig),
    exhaustMap(() => this.service.readIni()
      .pipe(
        map((result: PzServerReturn) => setIniConfig({config: result.msg})),
        catchError(error => {
          console.error(error);
          return of(serverStatusError());
        })
      )
    )
  ))

  forceStop = createEffect(() => this.actions$.pipe(
    ofType(sendServerAction),
    filter((command) => command.action == PzServerAction.FORCESTOP),
    exhaustMap(() => this.service.forceStop()
      .pipe(
        map((result: PzServerReturn) => setStatus({newStatus: null})),
        catchError(error => {
          console.error(error);
          return of(serverStatusError());
        })
      )
    )
  ))

  restart = createEffect(() => this.actions$.pipe(
    ofType(sendServerAction),
    filter((command) => command.action == PzServerAction.RESTART),
    exhaustMap(() => this.service.restart()
      .pipe(
        map((result: PzServerReturn) => setStatus({newStatus: null})),
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
