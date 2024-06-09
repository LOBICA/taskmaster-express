import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { TaskFormComponent } from './components/taskform/taskform.component';
import { Task } from './models/task.model';
import { TaskService } from './services/task.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { finalize } from 'rxjs';

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
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'taskmaster';
  tasks: Map<string, Task>;
  editableTask: Task | undefined | null;
  formDisabled = false;

  constructor(private taskService: TaskService) {
    this.tasks = new Map<string, Task>();
    this.loadTasks();
  }

  loadTasks() {
    this.formDisabled = true;
    this.taskService
      .getTasks()
      .pipe(finalize(() => (this.formDisabled = false)))
      .subscribe((tasks) => {
        this.tasks.clear();
        for (const task of tasks) {
          this.tasks.set(task.uuid, task);
        }
      });
  }

  addTask(task: Task) {
    this.formDisabled = true;
    this.taskService
      .addTask(task)
      .pipe(finalize(() => (this.formDisabled = false)))
      .subscribe((task) => {
        this.tasks.set(task.uuid, task);
      });
  }

  completeTask(task: Task) {
    task.status = 'done';
    this.taskService.editTask(task.uuid, task).subscribe((task) => {
      this.tasks.set(task.uuid, task);
      this.loadTasks();
    });
  }

  openEditor(task: Task) {
    this.editableTask = task;
  }

  cancelEdition() {
    this.editableTask = null;
  }

  updateTask(task: Task) {
    this.formDisabled = true;
    this.taskService
      .editTask(task.uuid, task)
      .pipe(finalize(() => (this.formDisabled = false)))
      .subscribe((task) => {
        this.tasks.set(task.uuid, task);
        this.cancelEdition();
      });
  }

  deleteTask(task_id: string) {
    this.taskService.deleteTask(task_id).subscribe(() => {
      this.tasks.delete(task_id);
    });
  }
}
