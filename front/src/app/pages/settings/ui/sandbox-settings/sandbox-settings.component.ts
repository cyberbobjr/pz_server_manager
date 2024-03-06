import {Component, OnInit} from '@angular/core';
import {Observable, tap} from "rxjs";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {getConfig, saveConfig} from "@pzstore/actions/server.actions";
import {FormBuilder, Validators} from "@angular/forms";
import {PzConfigTypeEnum} from "@core/interfaces/PzConfigFileType";

@Component({
  selector: 'app-sandbox-settings',
  templateUrl: './sandbox-settings.component.html',
  styleUrl: './sandbox-settings.component.scss'
})
export class SandboxSettingsComponent implements OnInit {
  sandboxSettings$: Observable<string | null> = this.store.select(store => store.pzStore.lua_sandbox)
    .pipe(
      tap(r => this.iniForm.patchValue({config: r as string}))
    );
  iniForm = this.fb.group({
    config: ['', Validators.required]
  })
  initialConfig: string | null = null;

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.store.dispatch(getConfig({configType: PzConfigTypeEnum.lua_sandbox}));
  }

  saveConfig() {
    this.store.dispatch(saveConfig({
      content: (this.iniForm.get('config')!.value)!,
      filetype: PzConfigTypeEnum.lua_sandbox
    }))
  }

  refreshConfig() {
    this.iniForm.patchValue({config: this.initialConfig});
  }
}

