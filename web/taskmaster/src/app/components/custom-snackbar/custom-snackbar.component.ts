import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { SnackBarDisplay, SnackBarService } from '../../services/snackBar.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-custom-snackbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './custom-snackbar.component.html',
  styleUrl: './custom-snackbar.component.scss'
})
export class CustomSnackbarComponent implements OnInit, OnDestroy {
  private unSubscribe$ = new Subject<void>();
  snacks: SnackBarDisplay[] = [];

  constructor(private snackBarService: SnackBarService){}

  ngOnInit(): void {
    this.snackBarService.snackbarDisplay$.pipe(takeUntil(this.unSubscribe$)).subscribe((snack) => {
      if (snack) {
        this.snacks.push(snack);
        this.setVanishTime(snack.id);
      }
    })
  }

  ngOnDestroy(): void {
    this.unSubscribe$.next();
    this.unSubscribe$.complete();
  }

  closeSelected(id: number) {
    this.removeSnack(id);
  }

  private setVanishTime(id: number): void {
    setTimeout(() => {
      if(this.snacks.length > 0) {
        this.removeSnack(id);
      } else {
        this.snackBarService.closeSnackbar();
      }
    }, 5000);
  }

  private removeSnack(id: number) {
    const index = this.snacks.findIndex((snack) => snack.id === id);
    if (index != -1) {
      this.snacks.splice(index, 1);
    }
    if (this.snacks.length < 1) {
      this.snackBarService.closeSnackbar();
    }
  }
}
