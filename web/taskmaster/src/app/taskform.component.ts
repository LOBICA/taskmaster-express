import { Component, EventEmitter, Input, Output } from '@angular/core';
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
    @Input() editableTask: Task | null | undefined

    @Output() addTaskEvent = new EventEmitter<Task>();
    @Output() saveTaskEvent = new EventEmitter<Task>();
    @Output() cancelEditionEvent = new EventEmitter();

    taskForm = new FormGroup({
        title: new FormControl<string>('', Validators.required),
        description: new FormControl<string>('')
    });

    addTask() {
        if (this.taskForm.valid) {
            if(this.editableTask) {
                this.editableTask.title = this.taskForm.value.title!
                this.editableTask.description = this.taskForm.value.description ?? ''

                console.log(this.editableTask)

                this.saveTaskEvent.emit(this.editableTask)
            }
            else {
                const task = new Task(
                    crypto.randomUUID(),
                    this.taskForm.value.title!,
                    this.taskForm.value.description
                )
                this.addTaskEvent.emit(task)
                this.taskForm.reset()
            }
        }
    }

    cancelEdition() {
        this.cancelEditionEvent.emit()
    }
}
