<template>
  <v-btn depressed height="66px" width="178px" @click="clickButton">
    <img :src='require("..\\assets\\roll.png")' alt="roll"/>
  </v-btn>
</template>

<script>
export default {
  name: 'RollButton',
  methods: {
    clickButton () {
      this.$emit("click");
    }
  },
}
</script>
