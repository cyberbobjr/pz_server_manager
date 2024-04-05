import {createSelector} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";

export const selectPzFeature = (state: { pzStore: PzStore }) => state.pzStore;

export const selectModpacks = createSelector(
  selectPzFeature,
  (state: PzStore) => state.modpacks
);
