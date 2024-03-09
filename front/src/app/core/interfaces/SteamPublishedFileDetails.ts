import {WorkshopItems} from "@core/interfaces/PzModsIni";

export interface SteamPublishedFileDetails {
  next_cursor?: string;
  total: number;
  publishedfiledetails: WorkshopItems[];
}
