import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";
import {PzStatus} from "../interfaces/PzStatus";
import {PzServerReturn} from "../interfaces/PzServerReturn";
import {PzConfigTypeEnum} from "@core/interfaces/PzConfigFileType";
import {SteamPublishedFileDetails} from "@core/interfaces/SteamPublishedFileDetails";
import {PzServerManagerConfig} from "@core/interfaces/PzServerManagerConfig";

@Injectable({
  providedIn: 'root'
})
export class PzServerService {

  constructor(private httpClient: HttpClient) {
  }

  getStatus(): Observable<PzStatus> {
    return this.httpClient.get<PzStatus>(`${environment.baseUrl}/server/status`)
  }

  sendCommand(command: string): Observable<PzServerReturn> {
    return this.httpClient.post<PzServerReturn>(`${environment.baseUrl}/server/command`, command);
  }

  forceStop(): Observable<PzServerReturn> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/forcestop`);
  }

  restart(): Observable<PzServerReturn> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/restart`);
  }

  start(): Observable<PzServerReturn> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/start`);
  }

  stop(): Observable<PzServerReturn> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/stop`);
  }

  saveSettings(content: string, filetype: PzConfigTypeEnum): Observable<PzServerReturn> {
    return this.httpClient.post<PzServerReturn>(`${environment.baseUrl}/server/config`, {
      content: content,
      type: filetype
    });
  }

  getSettings(filetype: PzConfigTypeEnum): Observable<PzServerReturn> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/config?content_type=${filetype}`);
  }

  getModsIni(): Observable<any> {
    return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/mods/ini`);
  }

  searchMods(text: string, cursor: string): Observable<SteamPublishedFileDetails> {
    return this.httpClient.post<SteamPublishedFileDetails>(`${environment.baseUrl}/mods/search`, {text, cursor});
  }

  saveMods(Mods: string[], WorkshopItems: string[], Maps: string[]): Observable<any> {
    return this.httpClient.post<SteamPublishedFileDetails>(`${environment.baseUrl}/server/mods`, {
      Mods,
      WorkshopItems,
      Maps
    });
  }

  checkStatus(workshopItemId: string): Observable<{ workshopItem: string; status: string }> {
    return this.httpClient.get<{
      workshopItem: string;
      status: string
    }>(`${environment.baseUrl}/server/task/${workshopItemId}`)
  }

  getTasksInProgress(): Observable<string[]> {
    return this.httpClient.get<string[]>(`${environment.baseUrl}/server/task/`);
  }

  getConfig(): Observable<PzServerManagerConfig> {
    return this.httpClient.get<PzServerManagerConfig>(`${environment.baseUrl}/config`);
  }

  saveManagerConfig(content: string): Observable<PzServerManagerConfig> {
    return this.httpClient.post<PzServerManagerConfig>(`${environment.baseUrl}/config`, content);
  }
}
