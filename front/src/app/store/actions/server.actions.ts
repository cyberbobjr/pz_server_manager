import {createAction, props} from "@ngrx/store";
import {PzStatus} from "../../core/interfaces/PzStatus";
import {PzServerAction} from "../../core/interfaces/PzServerAction";

export const getStatus = createAction('[PZ SERVER] - get status');
export const setStatus = createAction('[PZ SERVER] - set status', props<{ newStatus: PzStatus | null }>());
export const serverStatusError = createAction('[PZ SERVER] - status error')
export const sendCommand = createAction('[PZ SERVER] - send command', props<{ command: string }>());
export const setCommandResult = createAction('[PZ SERVER] - set command result', props<{ result: string }>());
export const getPlayersCount = createAction('[PZ SERVER] - get number of players');
export const setPlayersCount = createAction('[PZ SERVER] - set number of players', props<{ count: number }>());
export const getIniConfig = createAction('[PZ SERVER] - get ini config');
export const setIniConfig = createAction('[PZ SERVER] - set ini config', props<{ config: string }>());
export const sendServerAction = createAction('[PZ SERVER] - send action', props<{ action: PzServerAction }>());
