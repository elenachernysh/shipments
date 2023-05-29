import axios from "axios";
import store from "./store";

let refresh = false;

axios.interceptors.request.use(function (config) {
    config.headers.Authorization = `Bearer ${store.state.accessToken}`;
    return config;
});

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true;
        const {status, data} = await axios.post('/api/user/token/refresh/',
            {"refresh": store.state.refreshToken}, {headers:{ Authorization:""}});

        if (status === 200) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;
            store.dispatch('set_auth_tokens', {
                accessToken: response.data['access'],
                refreshToken: response.data['refresh']
            });
            return axios(error.config);
        }
    }
    refresh = false;
    return error;
});

export default axios;
