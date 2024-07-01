import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {
  private loadingStatus = new BehaviorSubject<boolean>(false);

  get status$() {
    return this.loadingStatus.asObservable();
  }

  enableLoadingStatus() {
    if (!this.loadingStatus.value) {
      this.loadingStatus.next(true);
    }
  }

  disableLoadingStatus() {
    if (this.loadingStatus.value) {
      this.loadingStatus.next(false);
    }
  }
}
