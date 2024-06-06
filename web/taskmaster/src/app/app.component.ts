import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { TaskFormComponent } from './taskform.component';
import { Task } from './task.model';
import { TaskService } from './task.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    MatCardModule,
    TaskFormComponent,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'taskmaster';
  tasks: Map<string, Task>;
  editableTask: Task | undefined | null

  constructor(private taskService: TaskService) {
    this.tasks = new Map<string, Task>()
    this.loadTasks()
  }

  loadTasks() {
    this.taskService.getTasks().subscribe(tasks => {
      this.tasks.clear()
      for(const task of tasks) {
        this.tasks.set(task.uuid, task)
      }
    })
  }

  addTask(task: Task) {
    this.taskService.addTask(task).subscribe(task => {
      this.tasks.set(task.uuid, task)
    });
  }

  openEditor(task: Task) {
    this.editableTask = task
  }

  cancelEdition() {
    this.editableTask = null
  }

  updateTask(task: Task) {
    this.taskService.editTask(task.uuid, task).subscribe(task => {
      this.tasks.set(task.uuid, task)
      this.cancelEdition()
    })
  }

  deleteTask(task_id: string) {
    this.taskService.deleteTask(task_id).subscribe(() => {
      this.tasks.delete(task_id)
    })
  }
}
