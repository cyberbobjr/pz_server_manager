import {createFeatureSelector, createSelector} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";

export const selectPzStore = createFeatureSelector<PzStore>('pzStore');

export const selectIniConfig = createSelector(
  selectPzStore,
  (state: PzStore) => {
    return {...state}.server_ini;
  }
);
