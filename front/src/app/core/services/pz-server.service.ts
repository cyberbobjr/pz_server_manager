import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class PzServerService {

  constructor(private httpClient: HttpClient) {
  }

  getStatus() {
    return this.httpClient.get<any>(`${environment.baseUrl}/server/status`)
  }
}
