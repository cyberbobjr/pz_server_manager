export interface PzConfigFileEnum {
  configType: string;
  url: string;
}

export enum PzConfigTypeEnum {
  server_ini = 'server_ini',
  lua_sandbox = 'lua_sandbox',
}

export const PzConfigFileType: { [key: string]: PzConfigFileEnum } = {
  server_ini: ({
    configType: 'server_ini',
    url: 'settings'
  }),
  lua_sandbox: ({
    configType: 'lua_sandbox',
    url: 'sandbox_settings'
  }),
}

