export const environment = {
    production: false,
    apiUrl: 'http://localhost:8001',
    facebookAppId: process.env["FB_CLIENT_ID"],
    deepLink: `oauth?client_id=${process.env["821367659917526"]}&redirect_uri=${process.env["FB_REDIRECT"]}&scope=email&response_type=token`,
};
