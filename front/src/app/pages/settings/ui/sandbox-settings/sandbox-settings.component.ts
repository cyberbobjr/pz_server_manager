import {Component} from '@angular/core';
import {SharedModule} from "@shared/shared.module";
import {Observable, tap} from "rxjs";
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {getSandboxSettings} from "@pzstore/actions/server.actions";
import {CommonModule} from "@angular/common";
import {FormBuilder, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-sandbox-settings',
  standalone: true,
  imports: [
    CommonModule,
    SharedModule,
    ReactiveFormsModule
  ],
  templateUrl: './sandbox-settings.component.html',
  styleUrl: './sandbox-settings.component.scss'
})
export class SandboxSettingsComponent {
  sandboxSettings$: Observable<string | null> = this.store.select(store => store.pzStore.sandboxConfig)
    .pipe(
      tap(r => this.iniForm.patchValue({config: r as string}))
    );
  iniForm = this.fb.group({
    config: ['', Validators.required]
  })

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {
    this.store.dispatch(getSandboxSettings());
  }
}

