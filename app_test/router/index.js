import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import AddProduct from '../views/AddProduct.vue'
import Customization from '../views/Customization.vue'
import Installation from '../views/Installation.vue'
import Analytics from '../views/Analytics.vue'
import paths from  './paths'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: paths.Dashboard,
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: paths.AddProduct,
      name: 'AddProduct',
      component: AddProduct
    },
    {
      path: paths.Customization,
      name: 'Customization',
      component: Customization
    },
    {
      path: paths.Installation,
      name: 'Installation',
      component: Installation
    },
    {
      path: paths.Analytics,
      name: 'Analytics',
      component: Analytics
    }
  ]
})

export default router
