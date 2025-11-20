import { createApp, createSSRApp, h } from 'vue'
import VueCookies from 'vue-cookies';

import App from './App.vue'
import router from './router/index.js'
import store from './store/store.js'

/*
const rootComponent = {
    render: () => h(App),
    components: { App }
}*/


export default function application() {
    const app = createApp(App)
    app.use(VueCookies)
    app.use(router)
    app.use(store)
    return { app, router, store }
}