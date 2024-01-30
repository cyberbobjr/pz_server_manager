import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Parser} from 'bulletin-board-code';
import {Observable, of, switchMap} from 'rxjs';
import {environment} from '../../../../environments/environment';
import {Mod} from '../../mods/api/Mod';

@Injectable({
  providedIn: 'root'
})
export class SteamService {
  private baseUrl: string = environment.baseUrl;
  private parser = new Parser();

  constructor(private httpClient: HttpClient) {
  }

  getLatestMods(): Observable<Mod[]> {
    return this.httpClient.get<any[]>(`${this.baseUrl}/steam/latest`)
               .pipe(
                 switchMap(mod => of(
                     mod.map(m => ({
                       ...m,
                       html_description: this.parser.toHTML(m.file_description),
                       vote: Math.round(m.vote_data.score * 10)
                     }))
                   )
                 ),
               )
  }

  searchMods(name: string): Observable<Mod[]> {
    return this.httpClient.post<any[]>(`${this.baseUrl}/steam/search`, {text: name})
               .pipe(
                 switchMap(mod => of(
                     mod.map(m => ({
                       ...m,
                       html_description: this.parser.toHTML(m.file_description),
                       vote: Math.round(m.vote_data.score * 10)
                     }))
                   )
                 ),
               )
  }
}
