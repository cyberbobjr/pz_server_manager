import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {FormBuilder} from "@angular/forms";
import {Observable} from "rxjs";
import {CommonModule} from "@angular/common";
import {getIniConfig} from "@pzstore/actions/server.actions";

@Component({
  selector: 'app-ini-server',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ini-server.component.html',
  styleUrl: './ini-server.component.scss'
})
export class IniServerComponent implements OnInit {
  iniConfig$: Observable<string | null> = this.store.select(store => store.pzStore.iniConfig);

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.store.dispatch(getIniConfig());
  }


}
