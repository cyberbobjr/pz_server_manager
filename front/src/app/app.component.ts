import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {loadServerConfig} from "@pzstore/actions/server.actions";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {

  constructor(private store: Store<{ pzStore: PzStore }>) {
    this.store.dispatch(loadServerConfig());
  }

  ngOnInit() {
  }
}
