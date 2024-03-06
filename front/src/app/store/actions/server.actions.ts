import {createAction, props} from "@ngrx/store";
import {PzStatus} from "@core/interfaces/PzStatus";
import {PzServerAction} from "@core/interfaces/PzServerAction";
import {PzConfigFileType, PzConfigTypeEnum} from "@core/interfaces/PzConfigFileType";

export const getStatus = createAction('[PZ SERVER] - get status');
export const setStatus = createAction('[PZ SERVER] - set status', props<{ newStatus: PzStatus | null }>());
export const serverStatusError = createAction('[PZ SERVER] - status error')
export const sendCommand = createAction('[PZ SERVER] - send command', props<{ command: string }>());
export const setCommandResult = createAction('[PZ SERVER] - set command result', props<{ result: string }>());
export const getPlayersCount = createAction('[PZ SERVER] - get number of players');
export const setPlayersCount = createAction('[PZ SERVER] - set number of players', props<{ count: number }>());
export const getConfig = createAction('[PZ SERVER] - get config', props<{ configType: PzConfigTypeEnum }>());
export const saveConfig = createAction('[PZ SERVER] - save config', props<{
  content: string;
  filetype: PzConfigTypeEnum
}>());
export const sendServerAction = createAction('[PZ SERVER] - send action', props<{ action: PzServerAction }>());
export const setConfig = createAction('[PZ SERVER] - set config', props<{
  content: string,
  configType: PzConfigTypeEnum
}>())
export const setIniConfig = createAction('[PZ SERVER] - set ini config', props<{ config: string }>());
