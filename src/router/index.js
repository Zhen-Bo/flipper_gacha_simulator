import Vue from 'vue';
import VueRouter from 'vue-router';

import flipper from '@/views/Flipper';
import history from '@/views/History';
import report from '@/views/Report';

import nav from '@/views/Nav';

Vue.use(VueRouter);

const routes = [
  {
    path: '/', name: 'Nav', component: nav, children: [
      { path: '/flipper', name: 'Flipper', component: flipper },
      { path: '/history', name: 'History', component: history },
      { path: '/report', name: 'Report', component: report },
      { path: '*', redirect: { name: 'Flipper' } }
    ]
  }
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
