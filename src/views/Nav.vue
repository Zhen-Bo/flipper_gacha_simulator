<template>
  <div>
        <v-tabs
            dark
            v-model="tab"
            align-with-title
        >
          <v-tabs-slider color="yellow"></v-tabs-slider>

          <v-tab
              v-for="item in items"
              :key="item.name"
          >
            {{ item.text }}
          </v-tab>
        </v-tabs>
    <v-tabs-items v-model="tab" class="grey lighten-3">
      <v-tab-item v-for="item in items" :key="item.name">
        <router-view :pool="item.name"></router-view>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import Api from '@/plugins/api';

export default {
  name: 'AppNav',
  data () {
    return {
      tab: null,
      items: [],
    };
  },
  created () {
    Api.pool().then((rs) => {
      for (let rsKey in rs) {
        let data = rs[rsKey];
        this.items.unshift({ name: rsKey, text: data.name, type: data.type });
      }
    });
  }
};
</script>
