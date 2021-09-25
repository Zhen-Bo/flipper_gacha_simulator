<template>
  <v-app>
<!--    <v-app-bar-->
<!--      app-->
<!--      color="primary"-->
<!--      dark-->
<!--    >-->
<!--    -->
<!--    </v-app-bar>-->

    <v-main>
      <router-view/>
    </v-main>
    <div style="height: 60px"></div>

    <v-bottom-navigation v-model="value"
                         color="primary"
                         fixed
                         grow
    >
      <v-btn :value="item.value" class="font-weight-black" v-for="item in bottomNav" :key="item.value" :to="{name: item.value}">
        <span>{{ item.name }}</span>

        <v-icon>{{ item.icon }}</v-icon>
      </v-btn>

    </v-bottom-navigation>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      value: 'flipper',
      bottomNav: [{name:'抽卡', icon:'mdi-drawing-box', value: 'Flipper'}, {name:'記錄', icon:'mdi-history', value: 'History'}, {name:'統計', icon:'mdi-chart-areaspline-variant', value: 'Report'}]
    };
  },
  created () {
    this.value = this.$route.name;
  }
};
</script>

<style>
.v-item-group.v-bottom-navigation .v-btn.v-size--default {
  height: inherit;
  background: #fafafa;
  padding: 0 1.3rem;
}
</style>
