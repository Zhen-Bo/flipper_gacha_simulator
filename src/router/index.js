import Vue from 'vue'
import VueRouter from 'vue-router'

import flipper from '../views/Flipper'
import history from '../views/History'
import report from '../views/Report'

Vue.use(VueRouter)

const routes = [
  { path: '/',  redirect: '/flipper' },
  {path: '/flipper', name: 'Flipper', component: flipper},
  {path: '/history', name: 'History', component: history},
  {path: '/report', name: 'Report', component: report},
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
