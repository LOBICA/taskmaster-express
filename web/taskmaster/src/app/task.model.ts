export class Task {
    uuid: string;
    title: string;
    description: string;
    status: string = 'pending';
    dueDate: string | null = null;
    mood: string = 'neutral';

    public constructor(
        uuid: string, title: string, description: string | null | undefined
    ) {
        this.uuid = uuid
        this.title = title
        this.description = description ?? ''
    }
  }
