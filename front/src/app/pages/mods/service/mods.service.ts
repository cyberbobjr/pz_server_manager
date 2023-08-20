import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Parser} from 'bulletin-board-code';
import {Observable, of, switchMap, tap} from 'rxjs';
import {environment} from '../../../../environments/environment';
import {Mod} from '../api/Mod';

@Injectable({
  providedIn: 'root'
})
export class ModsService {
  private baseUrl: string = environment.baseUrl;
  parser = new Parser();
  mods: Mod[] = [];
  mods$: Observable<Mod[]> = this.listMods()
                                 .pipe(
                                   switchMap(m => of(
                                       m.sort((a, b) => a.name.localeCompare(b.name))
                                        .map(mod => ({
                                          ...mod,
                                          html_description: this.parser.toHTML(mod.steam_data!.file_description),
                                          vote: Math.round(mod.steam_data!.vote_data.score * 10)
                                        }))
                                     )
                                   ),
                                   tap(m => this.mods = m)
                                 )

  constructor(private httpClient: HttpClient) {
  }

  listMods(): Observable<Mod[]> {
    return this.httpClient.get<Mod[]>(`${this.baseUrl}/mods/`);
  }

  listModpack(): Observable<string[]> {
    return this.httpClient.get<string[]>(`${this.baseUrl}/mods/modpack/`);
  }
}
