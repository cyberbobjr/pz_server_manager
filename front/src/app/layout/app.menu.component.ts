import {OnDestroy, OnInit} from '@angular/core';
import {Component} from '@angular/core';
import {Subscription} from 'rxjs';
import {ModpackService} from '../pages/mods/service/modpack.service';
import {LayoutService} from './service/app.layout.service';

@Component({
  selector: 'app-menu',
  templateUrl: './app.menu.component.html'
})
export class AppMenuComponent implements OnInit, OnDestroy {
  model: any[] = [];
  subscription: Subscription = new Subscription();

  constructor(public layoutService: LayoutService,
              private modpackService: ModpackService) {

  }

  ngOnInit() {
    this.subscription.add(this.modpackService
                              .modpacksContents$
                              .asObservable()
                              .subscribe(m => {
                                const menus = [];
                                for (const [key, value] of m) {
                                  menus.push(
                                    {
                                      label: key,
                                      badge: value.size,
                                      routerLink: ['/mods/modpackdetail/', key]
                                    }
                                  )
                                }
                                this.setMenu(menus);
                              })
    )
    this.setMenu([]);
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }


  private setMenu(modpackMenu: any[]) {
    this.model = [
      {
        label: 'Home',
        items: [
          {label: 'Dashboard', icon: 'pi pi-fw pi-home', routerLink: ['/']}
        ]
      },
      {
        label: 'Mods',
        items: [
          {
            label: 'Liste des mods', icon: 'pi pi-fw pi-id-card', routerLink: ['/mods']
          }
        ]
      },
      {
        label: 'Modpack',
        items: [...modpackMenu]
      }
    ]
  }
}
