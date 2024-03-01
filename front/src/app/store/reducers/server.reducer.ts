import {PzStatus} from "../../core/interfaces/PzStatus";
import {createReducer, on} from "@ngrx/store";
import {serverStatusError, setCommandResult, setStatus} from "../actions/server.actions";

export interface PzStore {
  status: PzStatus | null;
  commandResult: string | null;
}

export const initialPzStore: PzStore = {
  status: null,
  commandResult: null
}

export const pzReducer = createReducer(
  initialPzStore,
  on(setStatus, (state, {newStatus}) => ({...state, status: newStatus})),
  on(serverStatusError, (state) => ({...state, status: null})),
  on(setCommandResult, (state, {result}) => ({...state, commandResult: result}))
)
