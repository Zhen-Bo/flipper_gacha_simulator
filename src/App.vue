<template>
  <v-app style="background-color: #21252994">

    <v-main>
      <v-container style="max-width: 600px;background-color: #FFFFFF" class="pa-0">
        <router-view/>
        <div style="height: 60px;"></div>
      </v-container>
    </v-main>

    <v-bottom-navigation v-model="value"
                         color="primary"
                         fixed
                         grow
    >
      <v-btn :value="item.value" class="font-weight-black" v-for="item in bottomNav" :key="item.value" :to="{name: item.value}" @click="$vuetify.goTo(0,{duration:10,easing:'easeInOutCubic'})">
        <span>{{ item.name }}</span>

        <v-icon>{{ item.icon }}</v-icon>
      </v-btn>

    </v-bottom-navigation>

    <snackbar ref="snackbar"></snackbar>
  </v-app>
</template>

<script>

import Snackbar from '@/components/Snackbar';
export default {
  name: 'App',
  components: { Snackbar },
  data () {
    return {
      value: 'flipper',
      bottomNav: [{name:'抽卡', icon:'mdi-drawing-box', value: 'Flipper'}, {name:'記錄', icon:'mdi-history', value: 'History'}, {name:'統計', icon:'mdi-chart-areaspline-variant', value: 'Report'}]
    };
  },
  created () {
    this.value = this.$route.name;
  },
  mounted () {
    this.$root.$snackbar = this.$refs.snackbar;
  },
};
</script>

<style>
.v-item-group.v-bottom-navigation .v-btn.v-size--default {
  height: inherit;
  background: #fafafa;
  padding: 0 1.3rem;
}
</style>
