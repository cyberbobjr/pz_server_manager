import {Component, Inject} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {MaterialModule} from "@app-material/material.module";
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-dialog-del-mod-confirmation',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    MaterialModule
  ],
  templateUrl: './dialog-del-mod-confirmation.component.html',
  styleUrl: './dialog-del-mod-confirmation.component.scss'
})
export class DialogDelModConfirmationComponent {
  constructor(public dialogRef: MatDialogRef<DialogDelModConfirmationComponent>,
              @Inject(MAT_DIALOG_DATA) public data: { mod_name: string }) {
  }

  onNoClick(): void {
    this.dialogRef.close(false);
  }

  onOkClick(): void {
    this.dialogRef.close(true);
  }
}
