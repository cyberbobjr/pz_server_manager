import {Component, Input} from '@angular/core';
import {Item} from "../recipe-search.component";
import {MaterialModule} from "@app-material/material.module";
import {CommonModule} from "@angular/common";

@Component({
  selector: 'app-source-display',
  standalone: true,
  imports: [
    CommonModule,
    MaterialModule
  ],
  templateUrl: './source-display.component.html',
  styleUrl: './source-display.component.scss'
})
export class SourceDisplayComponent {
  @Input() items: Item[] = [];

  getClass(item: Item): string {
    return item.keep ? 'keep' : 'destroy';
  }
}
