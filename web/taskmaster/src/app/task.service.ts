import { Injectable, inject } from "@angular/core";
import { Task } from "./task.model";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class TaskService {
    http = inject(HttpClient)

    getTasks(): Observable<Task[]> {
         return this.http.get<Task[]>('http://localhost:8001/tasks')
    }

    addTask(task: Task): Observable<Task> {
        return this.http.post<Task>('http://localhost:8001/tasks', task);
    }
}
