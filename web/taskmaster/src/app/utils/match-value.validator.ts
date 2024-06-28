import { AbstractControl, FormGroup, ValidationErrors, ValidatorFn } from '@angular/forms';

export function MatchValue(controlName: string, matchingControlName: string): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const compareControl = control.get(controlName);
    const matchingControl = control.get(matchingControlName);

    if (!compareControl || !matchingControl) {
      return null;
    }
    return compareControl.value !== matchingControl.value ? { matchValue: true } : null;
  }
}