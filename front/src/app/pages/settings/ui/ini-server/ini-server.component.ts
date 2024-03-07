import {Component, OnDestroy, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {filter, Observable, Subscription} from "rxjs";
import {getConfig, saveConfig} from "@pzstore/actions/server.actions";
import {FormBuilder, Validators} from "@angular/forms";
import {selectIniConfig} from "@pzstore/selectors/server.selectors";
import {PzConfigTypeEnum} from "@core/interfaces/PzConfigFileType";

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
  initialConfig: string | null = null;
  loading$: Observable<boolean> = this.store.select((store) => store.pzStore.loading);

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
          this.initialConfig = r!;
          this.iniForm.patchValue({config: r});
          selectIniConfig.release();
        })
    )
    this.store.dispatch(getConfig({configType: PzConfigTypeEnum.server_ini}));
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  saveConfig() {
    this.store.dispatch(saveConfig({
      content: (this.iniForm.get('config')!.value)!,
      filetype: PzConfigTypeEnum.server_ini
    }))
  }

  refreshConfig() {
    this.iniForm.patchValue({config: this.initialConfig});
  }
}
