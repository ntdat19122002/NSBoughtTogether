import {createApp, h} from 'vue/dist/vue.esm-bundler';
import router from './router'
import App from './App.vue'
import 'ant-design-vue/dist/antd.css';
import { DatePicker } from 'ant-design-vue';
import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

// Create a new store instance.
const store = createStore({
    state () {
        return {
            activity:localStorage.getItem('activity'),
            products_bundle:JSON.parse(localStorage.getItem('products_bundle')),
            excluded_products_bundle:JSON.parse(localStorage.getItem('excluded_products_bundle'))
        }
    },
    plugins: [createPersistedState()]
})

var app = createApp({
    name: 'App',
    render: () => {
        return <App/>
    }
})

app.use(DatePicker);
app.use(router)
app.use(store)

app.mount('#app-id')

