import {Component, Inject} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";
import {FormsModule} from "@angular/forms";
import {MaterialModule} from "@app-material/material.module";
import {CommonModule} from "@angular/common";

interface ListItem {
  id: string;
  selected: boolean;
}

@Component({
  selector: 'app-dialog-add-mod-confirmation',
  templateUrl: './dialog-add-mod-confirmation.component.html',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    MaterialModule
  ],
  styleUrl: './dialog-add-mod-confirmation.component.scss'
})
export class DialogAddModConfirmationComponent {
  modsList: ListItem[] = [];
  mapsList: ListItem[] = [];

  constructor(public dialogRef: MatDialogRef<DialogAddModConfirmationComponent>,
              @Inject(MAT_DIALOG_DATA) public data: { mods: string, workshop: string, maps: string }) {
    this.modsList = data.mods.split(';').map(id => ({id, selected: false}));
    this.mapsList = data.maps.split(';').map(id => ({id, selected: false}));
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onOkClick(): void {
    const selectedMods = this.modsList.filter(item => item.selected).map(item => item.id).join(';');
    const selectedMaps = this.mapsList.filter(item => item.selected).map(item => item.id).join(';');

    this.dialogRef.close({mods: selectedMods, workshop: this.data.workshop, maps: selectedMaps});
  }
}
