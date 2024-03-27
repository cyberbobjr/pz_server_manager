import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {filter, Observable, Subscription} from "rxjs";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {selectManagerConfig} from "@pzstore/selectors/server.selectors";
import {saveServerManagerConfig} from "@pzstore/actions/server.actions";
import {PzServerManagerConfig} from "@core/interfaces/PzServerManagerConfig";

@Component({
  selector: 'app-manager-settings',
  templateUrl: './manager-settings.component.html',
  styleUrl: './manager-settings.component.scss'
})
export class ManagerSettingsComponent implements OnInit, OnDestroy {
  iniForm: FormGroup;
  iniConfig$: Observable<PzServerManagerConfig | null> | null = this.store.select(selectManagerConfig);
  subscription: Subscription = new Subscription();
  initialConfig: PzServerManagerConfig | null = null;
  loading$: Observable<boolean> = this.store.select((store) => store.pzStore.loading);

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
    this.iniForm = this.fb.group({
      config: [null, [Validators.required]] // Indique que config peut être null ou un objet conforme à PzServerManagerConfig
    });
  }

  ngOnInit(): void {
    this.subscription.add(
      this.iniConfig$!
        .pipe(
          filter(r => !!r)
        )
        .subscribe(r => {
          this.initialConfig = r!;
          this.iniForm.patchValue({config: JSON.stringify(r!, null, '\t')});
        })
    )
    // this.store.dispatch(loadServerManagerConfig());
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

  saveConfig() {
    this.store.dispatch(
      saveServerManagerConfig({
        content: JSON.parse(this.iniForm.get('config')!.value)!
      }))
  }

  refreshConfig() {
    this.iniForm.patchValue({config: this.initialConfig});
  }
}
