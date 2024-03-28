import {Component, EventEmitter, Input, OnDestroy, OnInit, Output, ViewEncapsulation,} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {Store} from "@ngrx/store";
import {interval, Observable, Subscription} from "rxjs";
import {getStatus} from "@pzstore/actions/server.actions";
import {PzStore} from "@pzstore/reducers/server.reducer";


@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  encapsulation: ViewEncapsulation.None,
})
export class HeaderComponent implements OnInit, OnDestroy {
  @Input() showToggle = true;
  @Input() toggleChecked = false;
  @Output() toggleMobileNav = new EventEmitter<void>();
  @Output() toggleMobileFilterNav = new EventEmitter<void>();
  @Output() toggleCollapsed = new EventEmitter<void>();

  status$: Observable<boolean | undefined>;
  subscription: Subscription = new Subscription();
  isServerMonitored$: Observable<boolean | undefined> = this.store.select((store) => store.pzStore.serverConfig?.pz.monitoring);

  constructor(public dialog: MatDialog,
              private store: Store<{ pzStore: PzStore }>) {
    this.store.dispatch(getStatus());
    this.status$ = this.store.select(store => {
      return store.pzStore.status?.server_started;
    });
  }

  ngOnInit(): void {
    this.subscription.add(interval(60000).subscribe(() => this.store.dispatch(getStatus())));
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }


}
