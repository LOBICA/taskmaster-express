import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { ConfirmDialog } from '../../interfaces/confirm-dialog.interface';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [MatDialogModule, CommonModule],
  templateUrl: './confirm-dialog.component.html',
  styleUrl: './confirm-dialog.component.scss'
})
export class ConfirmDialogComponent {
  dialog: ConfirmDialog;

  constructor(@Inject(MAT_DIALOG_DATA) public data: ConfirmDialog) {
    this.dialog = data;
  }
 }
