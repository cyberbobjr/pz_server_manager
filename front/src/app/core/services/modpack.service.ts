import {Injectable} from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class ModpackService {
  private apiUrl = environment.baseUrl; // Remplacez par l'URL de votre API

  constructor(private http: HttpClient) {
  }

  listModpacks(details: boolean = false): Observable<any> {
    return this.http.get(`${this.apiUrl}/modpacks?details=${details}`);
  }

  createModpack(packname: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/modpack/create`, {packname});
  }

  addModsToModpack(packname: string, workshopIds: string[], prefix: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/modpack/add_mods`, {packname, workshopIds, prefix});
  }

  toggleModInModpack(packname: string, workshop_id: string, mod_id: string, enabled: boolean): Observable<any> {
    return this.http.post(`${this.apiUrl}/modpack/toggle_mod`, {packname, workshop_id, mod_id, enabled});
  }

  changeWorkshopOrder(packname: string, workshop_id: string, new_position: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/modpack/change_workshop_order`, {packname, workshop_id, new_position});
  }

  changeModOrder(packname: string, workshop_id: string, mod_id: string, new_position: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/modpack/change_mod_order`, {packname, workshop_id, mod_id, new_position});
  }

  checkModpackUpdates(packname: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/modpack/${packname}/check_updates`);
  }
}
