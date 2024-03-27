export interface PzServerManagerConfig {
  "server": {
    "port": number;
    "host": string;
    "ssl_certfile": string;
    "ssl_keyfile": string;
  },
  "rcon": {
    "port": number;
    "host": string;
    "password": string;
  },
  "ssh": {
    "port": 21,
    "host": string;
    "username": string;
  },
  "auth": {
    "username": string;
    "password": string;
    "secret": string;
  },
  "pz": {
    "server_path": string;
    "pz_exe_path": string;
    "log_filename": string;
    "password": string;
    "monitoring": boolean;
  },
  "steam": {
    "apikey": string;
    "steamcmd_path": string;
    "cache_folder": string;
    "appid": number;
  },
  "discord": {
    "enable": boolean;
    "channel": number;
    "apikey": string;
  }
}
