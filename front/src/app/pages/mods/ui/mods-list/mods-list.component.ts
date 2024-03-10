import {Component, Input, OnInit, TemplateRef} from '@angular/core';
import {Observable, of} from "rxjs";
import {WorkshopItems} from "@core/interfaces/PzModsIni";

@Component({
  selector: 'app-mods-list',
  templateUrl: './mods-list.component.html',
  styleUrl: './mods-list.component.scss'
})
export class ModsListComponent implements OnInit {
  @Input() mods$: Observable<WorkshopItems[]> = of([]);
  // @ts-ignore
  @Input() actionsTemplate: TemplateRef<any>;
  columnsToDisplay = [
    "WorkshopItems",
    "Mods",
    "tags",
    "preview_url",
    "file_description",
    "actions"
  ];
  expandedStates: { [key: string]: boolean } = {}; // Utilisation d'un objet pour stocker l'état d'expansion par ligne

  constructor() {
  }

  ngOnInit(): void {
  }

  toggleDescription(rowId: string) {
    this.expandedStates[rowId] = !this.expandedStates[rowId];
  }

  isExpanded(rowId: string): boolean {
    return this.expandedStates[rowId];
  }
}
