import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { Message } from '../../models/message.model';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-chat',
  standalone: true,
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatListModule,
    MatIconModule,
  ],
})
export class ChatComponent {
  messageInput: string = '';

  messages: Message[] = Array<Message>();

  sendMessage(): void {
    if (this.messageInput) {
      const message = new Message(
        crypto.randomUUID(),
        this.messageInput,
        new Date(),
        'user',
      );
      this.messages.push(message);
      this.messageInput = '';
    }
  }
}
