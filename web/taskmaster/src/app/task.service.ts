import { Injectable } from "@angular/core";
import { Task } from "./task.model";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class TaskService {
    constructor(private http: HttpClient) {}

    getTasks(): Observable<Task[]> {
         return this.http.get<Task[]>(environment.apiUrl + '/tasks')
    }

    addTask(task: Task): Observable<Task> {
        return this.http.post<Task>(environment.apiUrl + '/tasks', task);
    }
}
