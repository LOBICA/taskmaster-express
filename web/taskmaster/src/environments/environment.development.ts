export const environment = {
    production: false,
    apiUrl: 'http://localhost:8001',
    facebookAppId: import.meta.env.FB_CLIENT_ID,
    deepLink: `oauth?client_id=${import.meta.env.FB_CLIENT_ID}&redirect_uri=${import.meta.env.FB_REDIRECT}&scope=email&response_type=token`,
};
