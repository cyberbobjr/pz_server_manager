import {Component} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {Observable} from "rxjs";

@Component({
  selector: 'app-tasks-icon',
  templateUrl: './tasks-icon.component.html',
  styleUrl: './tasks-icon.component.scss'
})
export class TasksIconComponent {
  inProgressCount$: Observable<number>;
  tasks$: Observable<string[]>;

  constructor(private store: Store<{ pzStore: PzStore }>) {
    this.inProgressCount$ = this.store.select((store) => store.pzStore.inProgressCount);
    this.tasks$ = this.store.select((store) => store.pzStore.downloadInProgress);
  }
}
