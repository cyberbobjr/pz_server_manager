import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";
import {PzStatus} from "../interfaces/PzStatus";
import {PzServerReturn} from "../interfaces/PzServerReturn";
import {getSandboxSettings, sendServerAction} from "@pzstore/actions/server.actions";

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

    readIni(): Observable<PzServerReturn> {
        return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/settings`);
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

    getSandboxSettings(): Observable<PzServerReturn> {
        return this.httpClient.get<PzServerReturn>(`${environment.baseUrl}/server/sandbox_settings`);
    }
}