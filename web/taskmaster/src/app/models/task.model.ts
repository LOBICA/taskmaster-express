export class Task {
    uuid: string;
    title: string;
    description: string;
    status = 'pending';
    dueDate: string | null = null;
    mood = 'neutral';

    public constructor(
        uuid: string, title: string, description: string | null | undefined
    ) {
        this.uuid = uuid
        this.title = title
        this.description = description ?? ''
    }
  }
