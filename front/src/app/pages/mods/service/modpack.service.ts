import {Injectable} from '@angular/core';
import {BehaviorSubject, firstValueFrom} from 'rxjs';
import {ModsService} from './mods.service';

@Injectable({
  providedIn: 'root'
})
export class ModpackService {
  modpacksContents: Map<string, Set<string>> = new Map<string, Set<string>>();
  modpacksContents$: BehaviorSubject<Map<string, Set<string>>> = new BehaviorSubject<Map<string, Set<string>>>(new Map());
  modpacks: string[] = [];
  modpacks$: BehaviorSubject<string[]> = new BehaviorSubject<string[]>([]);

  constructor(private modsService: ModsService) {
    firstValueFrom(this.modsService.listModpack())
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
  }
}
