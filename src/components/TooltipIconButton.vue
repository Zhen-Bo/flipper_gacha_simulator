<template>
  <v-tooltip bottom >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
          v-bind="attrs"
          v-on="on"
          icon
          @click="click"
      >
        <v-icon>
          {{ icon }}
        </v-icon>
      </v-btn>
    </template>
    <span>{{ message }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'TooltipIconButton',
  props: {
    icon: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      default: ''
    }
  },
  methods: {
    click () {
      this.$emit('click');
    }
  },
};
</script>
