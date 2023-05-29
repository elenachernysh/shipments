import { createApp } from 'vue'
import App from './App.vue'
import axios from "axios";
import store from "./store";
import router from "./router";

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

axios.defaults.baseURL = import.meta.env.API_URL || 'http://127.0.0.1:8000/';

const vuetify = createVuetify({
  components,
  directives,
})


const app = createApp(App);
app.use(router);
app.use(store);
app.use(vuetify);
app.mount('#app');
