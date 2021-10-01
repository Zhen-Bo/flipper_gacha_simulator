<template>
  <v-btn depressed height="66px" width="178px" @click="clickButton">
    <img :src='`${resourceURL}/static/roll.png`' alt="roll"/>
  </v-btn>
</template>

<script>
import API from '../plugins/api';

export default {
  name: 'RollButton',
  methods: {
    clickButton () {
      this.$emit("click");
    }
  },
  data () {
    return {
      resourceURL: API.resourceURL
    };
  },
}
</script>
