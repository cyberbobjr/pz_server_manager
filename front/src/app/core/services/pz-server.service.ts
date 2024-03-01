import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";
import {PzStatus} from "../interfaces/PzStatus";
import {PzServerReturn} from "../interfaces/PzServerReturn";

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
}
