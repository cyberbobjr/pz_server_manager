import {Component} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {MatInputModule} from "@angular/material/input";
import {CommonModule} from "@angular/common";
import {Observable} from "rxjs";
import {sendCommand} from "@pzstore/actions/server.actions";

@Component({
  selector: 'app-server-send-command',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    MatInputModule,
    CommonModule
  ],
  templateUrl: './server-send-command.component.html',
  styleUrl: './server-send-command.component.scss'
})
export class ServerSendCommandComponent {
  commandForm: FormGroup = this.fb.group({
    command: [null, [Validators.required]]
  })
  commandResult$: Observable<string | null> = this.store.select(store => store.pzStore.commandResult);

  constructor(private store: Store<{ pzStore: PzStore }>,
              private fb: FormBuilder) {
  }

  sendCommand() {
    this.store.dispatch(sendCommand({command: this.commandForm.value.command}));
  }
}
