import { Injectable } from "@angular/core";
import { Task } from "../models/task.model";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class TaskService {
    constructor(private http: HttpClient) {}

    getTasks(status="pending"): Observable<Task[]> {
         return this.http.get<Task[]>(environment.apiUrl + '/tasks?status=' + status)
    }

    addTask(task: Task): Observable<Task> {
        return this.http.post<Task>(environment.apiUrl + '/tasks', task);
    }

    getTask(task_id: string): Observable<Task> {
        return this.http.get<Task>(environment.apiUrl + '/tasks/' + task_id)
    }

    editTask(task_id: string, task: Task): Observable<Task> {
        return this.http.patch<Task>( environment.apiUrl + '/tasks/' + task_id, task)
    }

    deleteTask(task_id: string): Observable<null> {
        return this.http.delete<null>(environment.apiUrl + '/tasks/' + task_id)
    }
}
