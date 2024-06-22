import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { Subject, finalize, takeUntil } from 'rxjs';
import { TaskFormComponent } from '../taskform/taskform.component';
import { Task } from '../../models/task.model';
import { TaskService } from '../../services/task.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-tasks',
  standalone: true,
  imports: [
    MatCardModule,
    MatIconModule,
    MatButtonModule,
    TaskFormComponent,
  ],
  templateUrl: './tasks.component.html',
  styleUrl: './tasks.component.scss'
})
export class TasksComponent {
  tasks: Map<string, Task>;
  editableTask: Task | undefined | null;
  formDisabled = false;
  loggedIn = false;
  unsubscribe$ = new Subject<void>();


  constructor(
    private taskService: TaskService,
    private loginService: LoginService,
  ) {
    this.tasks = new Map<string, Task>();
  }

  ngOnInit(): void {
    this.loginService.loginStatus$.pipe(takeUntil(this.unsubscribe$)).subscribe((status) => {
      this.loggedIn = status;
      this.loadTasks();
    });
    const storedToken = localStorage.getItem('jwt');
    if (storedToken) {
      this.loginService.updateStatus(true);
    } else {
      this.loadTasks();
    }
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
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
      this.tasks.clear();
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
      this.cancelEdition();
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
