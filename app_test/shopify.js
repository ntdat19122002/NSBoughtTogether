import {createApp, h} from 'vue/dist/vue.esm-bundler';
import 'ant-design-vue/dist/antd.css';
import ShopifyBundle from "./components/ShopifyBundle.vue";



var app_bundle = createApp({
    name: 'AppShopify',
    render: () => {
        return <ShopifyBundle/>
    }
})

app_bundle.mount('#app-shopify-id')