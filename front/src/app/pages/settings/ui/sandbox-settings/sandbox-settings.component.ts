import {Component} from '@angular/core';
import {SharedModule} from "../../../../shared/shared.module";

@Component({
  selector: 'app-sandbox-settings',
  standalone: true,
  imports: [
    SharedModule
  ],
  templateUrl: './sandbox-settings.component.html',
  styleUrl: './sandbox-settings.component.scss'
})
export class SandboxSettingsComponent {

}
