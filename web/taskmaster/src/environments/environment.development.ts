export const environment = {
    production: false,
    apiUrl: 'http://localhost:8001',
    facebookAppId: '821367659917526',
    deepLink: `oauth?client_id=${process.env["821367659917526"]}&redirect_uri=${process.env["FB_REDIRECT"]}&scope=email`,
};
