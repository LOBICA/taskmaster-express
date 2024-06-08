import {
  Component,
  EventEmitter,
  Input,
  Output,
  ViewChild,
} from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import {
  FormGroup,
  FormControl,
  Validators,
  ReactiveFormsModule,
  FormGroupDirective,
} from '@angular/forms';
import { Task } from '../../models/task.model';

@Component({
  selector: 'app-taskform',
  standalone: true,
  imports: [
    MatSelectModule,
    MatInputModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatButtonModule,
  ],
  templateUrl: './taskform.component.html',
})
export class TaskFormComponent {
  @Input() set editableTask(task: Task | null | undefined) {
    if (task) {
      this.taskForm.setValue({
        title: task.title,
        description: task.description,
      });
      this.taskInEdition = task;
      this.taskForm.updateValueAndValidity();
    }
  }
  @Input() disabled = false;

  @Output() addTaskEvent = new EventEmitter<Task>();
  @Output() saveTaskEvent = new EventEmitter<Task>();
  @Output() cancelEditionEvent = new EventEmitter();

  taskInEdition?: Task;

  taskForm = new FormGroup({
    title: new FormControl<string>('', Validators.required),
    description: new FormControl<string>(''),
  });

  addTask(formDirective: FormGroupDirective) {
    if (this.taskForm.valid) {
      if (this.taskInEdition) {
        this.taskInEdition.title = this.taskForm.value.title!;
        this.taskInEdition.description = this.taskForm.value.description ?? '';

        console.log(this.taskInEdition);

        this.saveTaskEvent.emit(this.taskInEdition);
        this.resetFormValues(formDirective);
      } else {
        const task = new Task(
          crypto.randomUUID(),
          this.taskForm.value.title!,
          this.taskForm.value.description
        );
        this.addTaskEvent.emit(task);
        this.resetFormValues(formDirective);
      }
    }
  }

  cancelEdition() {
    this.cancelEditionEvent.emit();
  }

  private resetFormValues(formDirective: FormGroupDirective): void {
    this.taskInEdition = undefined;
    this.taskForm.reset();
    formDirective.resetForm();
  }
}
