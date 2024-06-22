import { Component, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { Message, ChatInput } from '../../models/message.model';
import { ChatService } from '../../services/chat.service';


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
  @Input() user: string = 'Guest';

  messageInput: string = '';
  messages: Message[] = Array<Message>();

  constructor(private chatService: ChatService) {
    this.chatService.connect();
    this.chatService.onMessage().subscribe((event: MessageEvent) => {
      if (event.data) {
        const message = JSON.parse(event.data) as Message;
        this.messages.push(message);
      }
    });
  }

  sendMessage(): void {
    if (this.messageInput) {
      const message = new Message(
        crypto.randomUUID(),
        this.messageInput,
        new Date(),
        this.user,
      );
      const chatInput = new ChatInput(message, this.messages);
      this.messages.push(message);
      this.chatService.send(chatInput);
      this.messageInput = '';
    }
  }
}
