import Vue from "vue";
import VueAnalytics from "vue-analytics";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import moment from "vue-moment";

Vue.config.productionTip = false;

Vue.use(VueAnalytics, {
  id: "UA-206510416-4",
  router,
  autoTracking: {
    pageviewOnLoad: false,
  },
});

Vue.use(moment);

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
