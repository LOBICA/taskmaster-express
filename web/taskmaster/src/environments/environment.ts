export const environment = {
    production: true,
    apiUrl: 'https://api.helpitdone.com',
    facebookAppId: process.env["FB_CLIENT_ID"],
    deepLink: `oauth?client_id=${process.env["FB_CLIENT_ID"]}&redirect_uri=${process.env["FB_REDIRECT"]}&scope=email&response_type=token`,
};
