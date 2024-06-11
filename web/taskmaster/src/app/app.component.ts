import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { TaskFormComponent } from './components/taskform/taskform.component';
import { LoginformComponent } from './components/loginform/loginform.component';
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
    LoginformComponent,
    MatButtonModule,
    MatIconModule,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  title = 'Taskmaster';
  tasks: Map<string, Task>;
  editableTask: Task | undefined | null;
  formDisabled = false;
  loggedIn = false;

  constructor(private taskService: TaskService) {
    this.tasks = new Map<string, Task>();
    this.loadTasks();
  }

  login(loginData: Object) {
    this.loggedIn = true;
  }

  loadTasks() {
    if (this.loggedIn) {
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
    } else {
      const task1 = new Task(crypto.randomUUID(), 'Register yourself', '');
      this.tasks.set(task1.uuid, task1);
      const task2 = new Task(crypto.randomUUID(), 'Start adding tasks!', '');
      this.tasks.set(task2.uuid, task2);
    }
  }

  addTask(task: Task) {
    if (this.loggedIn) {
      this.formDisabled = true;
      this.taskService
        .addTask(task)
        .pipe(finalize(() => (this.formDisabled = false)))
        .subscribe((task) => {
          this.tasks.set(task.uuid, task);
        });
    } else {
      this.tasks.set(task.uuid, task);
    }
  }

  completeTask(task: Task) {
    if (this.loggedIn) {
      task.status = 'done';
      this.taskService.editTask(task.uuid, task).subscribe((task) => {
        this.tasks.set(task.uuid, task);
        this.loadTasks();
      });
    } else {
      this.tasks.delete(task.uuid);
    }
  }

  openEditor(task: Task) {
    this.editableTask = task;
  }

  cancelEdition() {
    this.editableTask = null;
  }

  updateTask(task: Task) {
    if (this.loggedIn) {
      this.formDisabled = true;
      this.taskService
        .editTask(task.uuid, task)
        .pipe(finalize(() => (this.formDisabled = false)))
        .subscribe((task) => {
          this.tasks.set(task.uuid, task);
          this.cancelEdition();
        });
    } else {
      this.tasks.set(task.uuid, task);
    }
  }

  deleteTask(task_id: string) {
    if (this.loggedIn) {
      this.taskService.deleteTask(task_id).subscribe(() => {
        this.tasks.delete(task_id);
      });
    } else {
      this.tasks.delete(task_id);
    }
  }
}
