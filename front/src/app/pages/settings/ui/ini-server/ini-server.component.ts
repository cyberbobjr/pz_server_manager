import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {map, Observable, tap} from "rxjs";
import {CommonModule} from "@angular/common";
import {getIniConfig} from "@pzstore/actions/server.actions";
import {SharedModule} from "@shared/shared.module";
import {FormBuilder, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-ini-server',
  standalone: true,
  imports: [CommonModule, SharedModule, ReactiveFormsModule],
  templateUrl: './ini-server.component.html',
  styleUrl: './ini-server.component.scss'
})
export class IniServerComponent implements OnInit {
  iniForm = this.fb.group({
    config: ['', Validators.required]
  })
  iniConfig$: Observable<string | null> = this.store.select(store => store.pzStore.iniConfig)
    .pipe(
      tap(r => this.iniForm.patchValue({config: r as string}))
    );

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.store.dispatch(getIniConfig());
  }
}
