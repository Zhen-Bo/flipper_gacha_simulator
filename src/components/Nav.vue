<template>
  <v-toolbar
      color="primary"
      dark
      flat
  >
    <v-toolbar-title>彈射抽卡模擬</v-toolbar-title>
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
</template>

<script>
export default {
  name: 'AppNav',
  data () {
    return {
      tab: null,
      items: [
        { name: 'machine_police_girl', text: '警察池' }, { name: 'halfanv', text: '半周年禮黑' }
      ],
    };
  },
};
</script>
