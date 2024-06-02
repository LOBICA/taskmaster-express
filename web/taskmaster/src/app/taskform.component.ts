import { Component, EventEmitter, Output } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button'
import { FormsModule } from '@angular/forms';
import { Task } from './task.model';

@Component({
    selector: 'app-taskform',
    standalone: true,
    imports: [
        MatSelectModule,
        MatInputModule,
        MatFormFieldModule,
        FormsModule,
        MatButtonModule,
    ],
    templateUrl: './taskform.component.html'
})
export class TaskFormComponent {
    @Output() addTaskEvent = new EventEmitter<Task>();
    title = '';
    description = '';
    addTask() {
        let task = new Task(
            crypto.randomUUID(),
            this.title,
            this.description
        )
        this.addTaskEvent.emit(task)
        this.title = ''
        this.description = ''
    }
}
