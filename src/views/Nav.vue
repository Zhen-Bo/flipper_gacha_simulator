<template>
  <div>
    <v-toolbar
        color="primary"
        dark
        flat
    >
      <v-toolbar-title>彈射抽卡模擬</v-toolbar-title>

      <v-spacer></v-spacer>
      <v-btn icon href="https://github.com/Zhen-Bo/flipper_gacha_simulator/issues" target="_blank">
        <v-icon>mdi-bug</v-icon>
      </v-btn>

      <template v-slot:extension>
        <v-tabs
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
      </template>
    </v-toolbar>
    <v-tabs-items v-model="tab">
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
