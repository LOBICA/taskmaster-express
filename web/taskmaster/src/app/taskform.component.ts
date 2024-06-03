import { Component, EventEmitter, Output } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button'
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { Task } from './task.model';

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
    templateUrl: './taskform.component.html'
})
export class TaskFormComponent {
    @Output() addTaskEvent = new EventEmitter<Task>();
    taskForm = new FormGroup({
        title: new FormControl<string>('', Validators.required),
        description: new FormControl<string>('')
    });
    addTask() {
        let task = new Task(
            crypto.randomUUID(),
            this.taskForm.value.title!,
            this.taskForm.value.description
        )
        this.addTaskEvent.emit(task)
        this.taskForm.reset()
    }
}
