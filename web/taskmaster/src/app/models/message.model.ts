export class Message {
    constructor(
        public uuid: string,
        public text: string,
        public timestamp: Date,
        public sender: string,
    ) {}
}
