import {PzStatus} from "@core/interfaces/PzStatus";
import {createReducer, on} from "@ngrx/store";
import {
  addMods, deleteMods,
  getConfig,
  saveConfig, saveMods,
  serverStatusError,
  setCommandResult,
  setConfig,
  setIniConfig,
  setModsIni,
  setPlayersCount,
  setSearchedMods,
  setStatus
} from "../actions/server.actions";
import {PzModsIni, WorkshopItems} from "@core/interfaces/PzModsIni";

export interface PzStore {
  status: PzStatus | null;
  commandResult: string | null;
  playerCount: number;
  server_ini: string | null;
  lua_sandbox: string | null;
  loading: boolean;
  mods_installed: PzModsIni | null;
  mods_searched: WorkshopItems[];
}

export const initialPzStore: PzStore = {
  status: null,
  commandResult: null,
  playerCount: 0,
  server_ini: null,
  lua_sandbox: null,
  loading: false,
  mods_installed: null,
  mods_searched: []
}

export const pzReducer = createReducer(
  initialPzStore,
  on(setStatus, (state, {newStatus}) => ({...state, status: newStatus})),
  on(serverStatusError, (state) => ({...state, status: null})),
  on(getConfig, (state) => ({...state, loading: true})),
  on(saveMods, (state) => ({...state, loading: true})),
  on(saveConfig, (state) => ({...state, loading: true})),
  on(setCommandResult, (state, {result}) => ({...state, commandResult: result})),
  on(setIniConfig, (state, {config}) => ({...state, iniConfig: config})),
  on(setPlayersCount, (state, {count}) => ({...state, playerCount: count})),
  on(setConfig, (state, {content, configType}) => ({...state, loading: false, [configType]: content})),
  on(setModsIni, (state: PzStore, {mods}) => ({...state, mods_installed: mods, loading: false})),
  on(setSearchedMods, (state: PzStore, {mods}) => ({...state, mods_searched: mods})),
  on(addMods, (state: PzStore, {modsId, workShopdId, mapsId}) => {
    let newState = {...state};

    // Traitement des mods seulement si modsId n'est pas vide
    if (modsId) {
      const mods: string[] = modsId.split(';');
      if (mods.length > 0) {
        const newMods = [...(newState.mods_installed?.Mods_ini || [])];
        mods.filter(m => newMods.indexOf(m) === -1).forEach(m => newMods.push(m));
        newState = {
          ...newState,
          mods_installed: {
            ...newState.mods_installed!,
            Mods_ini: newMods,
          },
        };
      }
    }

    // Traitement des maps seulement si mapsId n'est pas vide
    if (mapsId) {
      const maps: string[] = mapsId.split(';');
      if (maps.length > 0) {
        const newMaps = [...(newState.mods_installed?.Maps_ini || [])];
        maps.filter(m => newMaps.indexOf(m) === -1).forEach(m => newMaps.push(m));
        newState = {
          ...newState,
          mods_installed: {
            ...newState.mods_installed!,
            Maps_ini: newMaps,
          },
        };
      }
    }

    // Ajout de workShopdId
    const newWorkshop = [...(newState.mods_installed?.Workshop_ini || []), workShopdId];
    newState = {
      ...newState,
      mods_installed: {
        ...newState.mods_installed!,
        Workshop_ini: newWorkshop,
      },
    };

    return newState;
  }),
  on(deleteMods, (state: PzStore, {modsId, workShopdId, mapsId}) => {
    let newState = {...state};

    // Traitement des mods seulement si modsId n'est pas vide
    if (modsId) {
      const modsToRemove: string[] = modsId.split(';');
      const currentMods = newState.mods_installed?.Mods_ini || [];
      const newMods = currentMods.filter(m => !modsToRemove.includes(m));
      newState = {
        ...newState,
        mods_installed: {
          ...newState.mods_installed!,
          Mods_ini: newMods,
        },
      };
    }

    if (mapsId) {
      const mapsToRemove: string[] = mapsId.split(';');
      const currentMaps = newState.mods_installed?.Maps_ini || [];
      const newMaps = currentMaps.filter(m => !mapsToRemove.includes(m));
      newState = {
        ...newState,
        mods_installed: {
          ...newState.mods_installed!,
          Maps_ini: newMaps,
        },
      };
    }

    if (workShopdId) {
      const currentWorkshops = newState.mods_installed?.Workshop_ini || [];
      const newWorkshop = currentWorkshops.filter(w => w !== workShopdId);
      const currentWorkshopItems: WorkshopItems[] = newState.mods_installed?.workshop_items || [];
      const newWorkshopItems: WorkshopItems[] = currentWorkshopItems.filter(w => w.steam_data.publishedfileid !== workShopdId);
      newState = {
        ...newState,
        mods_installed: {
          ...newState.mods_installed!,
          Workshop_ini: newWorkshop,
          workshop_items: newWorkshopItems
        },
      };
    }

    return newState;
  })
)
