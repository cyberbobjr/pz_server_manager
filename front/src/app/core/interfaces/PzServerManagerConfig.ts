export interface PzServerManagerConfig {
  "server": {
    "port": number;
    "host": string;
  },
  "rcon": {
    "port": number;
    "host": string;
  },
  "ssh": {
    "port": 21,
    "host": string;
    "username": string;
  },
  "auth": {
    "username": string;
    "password": string;
  },
  "pz": {
    "server_path": string;
    "pz_exe_path": string;
    "log_filename": string;
    "monitoring": boolean;
  },
  "steam": {
    "steamcmd_path": string;
    "cache_folder": string;
    "appid": number;
  },
  "discord": {
    "enable": boolean;
    "channel": number;
  }
}
