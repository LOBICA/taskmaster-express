export class Message {
    constructor(
        public uuid: string,
        public text: string,
        public timestamp: Date,
        public sender: string,
    ) {}
}

export class ChatInput {
    constructor(
        public message: Message,
        public history: Message[],
    ) {}
}
