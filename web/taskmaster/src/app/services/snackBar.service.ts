import { Injectable } from '@angular/core';
import { BehaviorSubject, take } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CustomSnackbarComponent } from '../components/custom-snackbar/custom-snackbar.component';

export interface SnackBarDisplay {
  id: number;
  text: string;
  type: SnackBarType;
}

export type SnackBarType = 'success' | 'warning' | 'error';

@Injectable({
  providedIn: 'root'
})
export class SnackBarService {
  snackbarOpened = false;
  index = 0;
  snackbarDisplay$ = new BehaviorSubject<SnackBarDisplay | null>(null);  

  constructor(private snackBar: MatSnackBar) { }

  openSnackbar(msg: string, type: SnackBarType): void {
    this.updateSnack(msg, type);
    if (!this.snackbarOpened) {
      this.snackbarOpened = true;
      const matReference = this.snackBar.openFromComponent(CustomSnackbarComponent, {
        horizontalPosition: 'start',
        verticalPosition: 'bottom',
        panelClass: 'custom-snack'
      });
      matReference.afterDismissed().pipe(take(1)).subscribe(() => this.snackbarOpened = false);
    }
  }

  closeSnackbar(): void {
    this.snackBar.dismiss();
  }

  private updateSnack(msg: string, type: SnackBarType): void {
    this.snackbarDisplay$.next({
      id: this.index,
      text: msg,
      type: type
    });
    this.index++;
  }
}
