<template>
  <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="-1"
      mobile-breakpoint="0"
      hide-default-footer
  >
    <template v-slot:foot v-if="rollTotal > 0">
      <tr>
        <td></td>
        <td></td>
        <td colspan="2" class="text-right">
          你已抽取{{ rollTotal }}次
        </td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: 'StarReport',
  props: {
    rollTotal: {
      type: Number,
      default: 0
    },
    desserts:{
      type: Array
    }
  },
  data () {
    return {
      headers: [
        {
          text: '',
          align: 'start',
          sortable: false,
          value: 'title',
        },
        { text: '5星 Up', value: 'star5_up', sortable: false, align: 'end' },
        { text: '5星', value: 'star5', sortable: false, align: 'end' },
        { text: '4星', value: 'star4', sortable: false, align: 'end' },
        { text: '3星', value: 'star3', sortable: false, align: 'end' }
      ],
    };
  },
};
</script>
