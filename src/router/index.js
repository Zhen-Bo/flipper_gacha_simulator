import Vue from 'vue'
import VueRouter from 'vue-router'

import flipper from '../views/Flipper'

Vue.use(VueRouter)

const routes = [
  { path: '/',  redirect: '/flipper' },
  {path: '/flipper', name: 'Flipper', component: flipper}
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
