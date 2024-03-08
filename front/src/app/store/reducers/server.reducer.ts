import {PzStatus} from "@core/interfaces/PzStatus";
import {createReducer, on} from "@ngrx/store";
import {
  getConfig, saveConfig,
  serverStatusError,
  setCommandResult,
  setConfig,
  setIniConfig, setModsIni,
  setPlayersCount,
  setStatus
} from "../actions/server.actions";
import {PzModsIni} from "@core/interfaces/PzModsIni";

export interface PzStore {
  status: PzStatus | null;
  commandResult: string | null;
  playerCount: number;
  server_ini: string | null;
  lua_sandbox: string | null;
  loading: boolean;
  mods_ini: PzModsIni | null;
}

export const initialPzStore: PzStore = {
  status: null,
  commandResult: null,
  playerCount: 0,
  server_ini: null,
  lua_sandbox: null,
  loading: false,
  mods_ini: null
}

export const pzReducer = createReducer(
  initialPzStore,
  on(setStatus, (state, {newStatus}) => ({...state, status: newStatus})),
  on(serverStatusError, (state) => ({...state, status: null})),
  on(getConfig, (state) => ({...state, loading: true})),
  on(saveConfig, (state) => ({...state, loading: true})),
  on(setCommandResult, (state, {result}) => ({...state, commandResult: result})),
  on(setIniConfig, (state, {config}) => ({...state, iniConfig: config})),
  on(setPlayersCount, (state, {count}) => ({...state, playerCount: count})),
  on(setConfig, (state, {content, configType}) => ({...state, loading: false, [configType]: content})),
  on(setModsIni, (state: PzStore, {mods}) => ({...state, mods_ini: mods}))
)
