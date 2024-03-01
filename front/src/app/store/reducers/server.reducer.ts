import {PzStatus} from "../../core/interfaces/PzStatus";
import {createReducer, on} from "@ngrx/store";
import {serverStatusError, setCommandResult, setIniConfig, setPlayersCount, setStatus} from "../actions/server.actions";

export interface PzStore {
  status: PzStatus | null;
  commandResult: string | null;
  playerCount: number;
  iniConfig: string | null;
}

export const initialPzStore: PzStore = {
  status: null,
  commandResult: null,
  playerCount: 0,
  iniConfig: null
}

export const pzReducer = createReducer(
  initialPzStore,
  on(setStatus, (state, {newStatus}) => ({...state, status: newStatus})),
  on(serverStatusError, (state) => ({...state, status: null})),
  on(setCommandResult, (state, {result}) => ({...state, commandResult: result})),
  on(setIniConfig, (state, {config}) => ({...state, iniConfig: config})),
  on(setPlayersCount, (state, {count}) => ({...state, playerCount: count})),
)
