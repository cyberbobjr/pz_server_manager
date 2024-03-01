import { Component } from '@angular/core';
import {MaterialModule} from "../../../../material.module";
import {IniServerComponent} from "../../ui/ini-server/ini-server.component";

@Component({
  selector: 'app-index',
  standalone: true,
  imports: [
    MaterialModule,
    IniServerComponent
  ],
  templateUrl: './index.component.html',
  styleUrl: './index.component.scss'
})
export class IndexComponent {

}
