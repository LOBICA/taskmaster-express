export const environment = {
    production: true,
    apiUrl: 'https://api.helpitdone.com',
    facebookAppId: '821367659917526',
    deepLink: `oauth?client_id=${process.env["821367659917526"]}&redirect_uri=${process.env["FB_REDIRECT"]}&scope=email`,
};
