export interface Modpack {
  packname: string;
  mods: ModDetails[];
  created_at: string;
  last_updated: string;
}

export interface ModDetails {
  workshop_id: string;
  modIds: ModIdDetails[];
}

export interface ModIdDetails {
  id: string;
  enabled: boolean;
  // Vous pouvez ajouter d'autres détails spécifiques au mod ici,
  // comme le nom du mod, une description, etc.
}
