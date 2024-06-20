import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private socket: Subject<MessageEvent>;

  constructor() {
    this.socket = new Subject();
  }

  public connect(): void {
    const ws = new WebSocket(environment.apiUrl + '/chat');

    this.socket.subscribe({
      next: (data: any) => {
        if(data && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(data));
        }
      },
      error: (err: ErrorEvent) => console.error('WebSocket error:', err),
      complete: () => ws.close()
    });

    ws.onmessage = (event) => this.socket.next(event);
    ws.onerror = (event) => this.socket.error(event);
    ws.onclose = (event) => this.socket.complete();
  }

  public send(data: any): void {
    if (data) {
      this.socket.next(data);
    }
  }

  public onMessage(): Observable<MessageEvent> {
    return this.socket.asObservable();
  }
}
