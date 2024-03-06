import {PzStatus} from "@core/interfaces/PzStatus";
import {createReducer, on} from "@ngrx/store";
import {
  serverStatusError,
  setCommandResult,
  setConfig,
  setIniConfig,
  setPlayersCount,
  setStatus
} from "../actions/server.actions";

export interface PzStore {
  status: PzStatus | null;
  commandResult: string | null;
  playerCount: number;
  server_ini: string | null;
  lua_sandbox: string | null;
}

export const initialPzStore: PzStore = {
  status: null,
  commandResult: null,
  playerCount: 0,
  server_ini: null,
  lua_sandbox: null,
}

export const pzReducer = createReducer(
  initialPzStore,
  on(setStatus, (state, {newStatus}) => ({...state, status: newStatus})),
  on(serverStatusError, (state) => ({...state, status: null})),
  on(setCommandResult, (state, {result}) => ({...state, commandResult: result})),
  on(setIniConfig, (state, {config}) => ({...state, iniConfig: config})),
  on(setPlayersCount, (state, {count}) => ({...state, playerCount: count})),
  on(setConfig, (state, {content, configType}) => ({...state, [configType]: content}))
)
