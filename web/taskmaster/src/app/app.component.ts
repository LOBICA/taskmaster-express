import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MatListModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'taskmaster';
  tasks = [
    {
      'uuid': '1234',
      'title': 'test 1',
      'description': 'this is a task',
      'status': 'pending',
      'due': null,
      'mood': 'neutral'
    },
    {
      'uuid': '4567',
      'title': 'test 2',
      'description': 'this is another task',
      'status': 'pending',
      'due': null,
      'mood': 'neutral'
    }
  ];
}
