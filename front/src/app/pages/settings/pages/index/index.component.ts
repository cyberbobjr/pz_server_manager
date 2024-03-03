import { Component } from '@angular/core';
import {MaterialModule} from "../../../../material.module";
import {IniServerComponent} from "../../ui/ini-server/ini-server.component";
import {SandboxSettingsComponent} from "../../ui/sandbox-settings/sandbox-settings.component";
import {SharedModule} from "../../../../shared/shared.module";

@Component({
  selector: 'app-index',
  standalone: true,
  imports: [
    MaterialModule,
    IniServerComponent,
    SandboxSettingsComponent,
    SharedModule
  ],
  templateUrl: './index.component.html',
  styleUrl: './index.component.scss'
})
export class IndexComponent {

}
