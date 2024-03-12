import {createFeatureSelector, createSelector} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {PzModsIni} from "@core/interfaces/PzModsIni";

export const selectPzStore = createFeatureSelector<PzStore>('pzStore');
export const selectIniConfig = createSelector(
  selectPzStore,
  (state: PzStore) => {
    return {...state}.server_ini;
  }
);
export const selectModsInstalled = createSelector(
  selectPzStore,
  (state: PzStore) => state.mods_installed
);

// Exemples de sélecteurs pour accéder à Mods_ini, Workshop_ini, et Maps_ini (si disponible) dans mods_installed
export const selectModsIni = createSelector(
  selectModsInstalled,
  (mods_installed) => mods_installed?.Mods_ini ?? []
);

export const selectWorkshopIni = createSelector(
  selectModsInstalled,
  (mods_installed) => mods_installed?.Workshop_ini ?? []
);

// Supposons que Maps_ini est le champ pour mapsId, ajustez selon la structure réelle de PzModsIni
export const selectMapsIni = createSelector(
  selectModsInstalled,
  (mods_installed) => mods_installed?.Maps_ini ?? [] // Remplacez 'Maps_ini' par le champ réel pour mapsId
);
