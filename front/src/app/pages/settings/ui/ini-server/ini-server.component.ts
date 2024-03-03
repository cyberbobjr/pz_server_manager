import {Component, OnDestroy, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {filter, Observable, Subscription} from "rxjs";
import {getIniConfig, setIniConfig} from "@pzstore/actions/server.actions";
import {FormBuilder, Validators} from "@angular/forms";
import {selectIniConfig} from "@pzstore/selectors/server.selectors";

@Component({
  selector: 'app-ini-server',
  templateUrl: './ini-server.component.html',
  styleUrl: './ini-server.component.scss'
})
export class IniServerComponent implements OnInit, OnDestroy {
  iniForm = this.fb.group({
    config: ['', Validators.required]
  })
  iniConfig$: Observable<string | null> | null = null;
  subscription: Subscription = new Subscription();

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.iniConfig$ = this.store.select(selectIniConfig);
    this.subscription.add(
      this.iniConfig$
        .pipe(
          filter(r => !!r)
        )
        .subscribe(r => {
          this.iniForm.patchValue({config: r});
          selectIniConfig.release();
        })
    )
    this.store.dispatch(getIniConfig());
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  saveConfig() {
    this.store.dispatch(setIniConfig({config: (this.iniForm.get('config')!.value)!}))
  }

  refreshConfig() {
    this.store.dispatch(getIniConfig());
  }
}
