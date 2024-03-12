export interface WorkshopTag {
  tag: string;
  display_name: string;
}

export interface WorkshopItems {
  Mods: string[];
  Maps: string[];
  WorkshopItems: string[];
  steam_data: SteamData
}

export interface SteamData {
  Mods?: string[]; // rustine
  Maps?: string[]; // rustine
  publishedfileid: string;
  file_size: string;
  preview_url: string;
  title: string;
  file_description: string;
  time_created: number;
  time_updated: number;
  vote_data: {
    score: number;
    votes_up: number;
    votes_down: number;
  };
  tags: WorkshopTag[];
}

export interface PzModsIni {
  Mods_ini: string[];
  Workshop_ini: string[];
  Maps_ini: string[];
  workshop_items: WorkshopItems[]
}
