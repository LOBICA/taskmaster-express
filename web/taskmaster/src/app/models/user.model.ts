export class User {
    constructor(
        public uuid: string | null,
        public name: string,
        public email: string,
        public password: string | null = null,
    ) {}
}
