import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {BehaviorSubject, firstValueFrom, Observable} from 'rxjs';
import {environment} from '../../../../environments/environment';
import {ModpackDetail} from '../api/Mod';
import {ModsService} from './mods.service';

@Injectable({
  providedIn: 'root'
})
export class ModpackService {
  private baseUrl: string = environment.baseUrl;
  modpacksContents: Map<string, Set<string>> = new Map<string, Set<string>>();
  modpacksContents$: BehaviorSubject<Map<string, Set<string>>> = new BehaviorSubject<Map<string, Set<string>>>(new Map());
  modpacks: string[] = [];
  modpacks$: BehaviorSubject<string[]> = new BehaviorSubject<string[]>([]);

  constructor(private modsService: ModsService,
              private httpClient: HttpClient) {
    firstValueFrom(this.listModpack())
      .then(m => {
        this.modpacks = m;
        this.modpacks$.next(m);
        m.forEach(modpackname => this.initModpack(modpackname));
      });
  }

  initModpack(modpackname: string) {
    this.modpacksContents.set(modpackname, new Set());
    this.modpacksContents$.next(this.modpacksContents);
  }

  addModIdToModpack(modpackname: string, modId: string) {
    let modIds: Set<string> | undefined = this.modpacksContents.get(modpackname);
    if (!modIds) {
      modIds = new Set<string>();
    }
    this.modpacksContents.set(modpackname, modIds.add(modId));
    this.modpacksContents$.next(this.modpacksContents);
    return this.httpClient.post<string[]>(`${this.baseUrl}/mods/modpack/`, {
      mods: [modId],
      packname: modpackname,
      prefix: modpackname
    });
  }

  listModpack(): Observable<string[]> {
    return this.httpClient.get<string[]>(`${this.baseUrl}/mods/modpack/`);
  }

  getModpackDetails(modpackname: string): Observable<ModpackDetail[]> {
    return this.httpClient.get<ModpackDetail[]>(`${this.baseUrl}/mods/modpack/?packname=${modpackname}`);
  }
}
