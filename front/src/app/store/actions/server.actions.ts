import {createAction, props} from "@ngrx/store";
import {PzStatus} from "../../core/interfaces/PzStatus";

export const getStatus = createAction('[PZ SERVER] - get status');
export const setStatus = createAction('[PZ SERVER] - set status', props<{ newStatus: PzStatus }>());
export const serverStatusError = createAction('[PZ SERVER] - status error')
export const sendCommand = createAction('[PZ SERVER] - send command', props<{ command: string }>());
export const setCommandResult = createAction('[PZ SERVER] - set command result', props<{ result: string }>());
