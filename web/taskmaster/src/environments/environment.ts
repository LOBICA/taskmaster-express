export const environment = {
    production: true,
    apiUrl: 'https://api.helpitdone.com',
    facebookAppId: import.meta.env.FB_CLIENT_ID,
    deepLink: `oauth?client_id=${import.meta.env.FB_CLIENT_ID}&redirect_uri=${import.meta.env.FB_REDIRECT}&scope=email&response_type=token`,
};
