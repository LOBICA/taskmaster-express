import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { TaskFormComponent } from './taskform.component';
import { Task } from './task.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MatListModule, TaskFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'taskmaster';
  tasks = Array<Task>();
  addTask(task: Task) {
    this.tasks.push(task)
  }
}
