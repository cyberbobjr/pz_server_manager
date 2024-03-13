import {createAction, props} from "@ngrx/store";
import {PzStatus} from "@core/interfaces/PzStatus";
import {PzServerAction} from "@core/interfaces/PzServerAction";
import {PzConfigTypeEnum} from "@core/interfaces/PzConfigFileType";
import {WorkshopItems} from "@core/interfaces/PzModsIni";
import {editor} from "monaco-editor";

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
export const loadModsIni = createAction('[PZ SERVER] - get mods ini');
export const setModsIni = createAction('[PZ SERVER] - set mods ini', props<{ mods: any }>());
export const searchMods = createAction('[PZ SERVER] - search mods', props<{ cursor?: string, text?: string }>())
export const setSearchedMods = createAction('[PZ SERVER] - set searched mods', props<{ mods: WorkshopItems[] }>())
export const addMods = createAction('[PZ SERVER] - add mods', props<{
  modsId: string,
  workShopdId: string,
  mapsId: string
}>())
export const deleteMods = createAction('[PZ SERVER] - delete mods', props<{
  modsId: string,
  workShopdId: string,
  mapsId: string,
}>())
export const saveMods = createAction('[PZ SERVER] - save mods');
export const loadInProgressTasksSuccess = createAction('[PZ SERVER] - Load In Progress Tasks Success', props<{
  tasks: string[]
}>());
