<template>
  <v-data-table
      :headers="headers"
      :items="desserts"
      :items-per-page="-1"
      hide-default-footer
      mobile-breakpoint="0"
      sort-by="total"
      :sort-desc="true"
  >
    <template v-slot:item.character="{ item }">
      <character-icon
          class="ma-2"
          style="width: 86px;"
          :attri="item.attri"
          :name="item.name"
          :id="item.id"
          :rarity="item.rarity"/>
    </template>

  </v-data-table>
</template>

<script>
import CharacterIcon from '@/components/CharacterIcon';

export default {
  name: 'CharacterReport',
  components: { CharacterIcon },
  props: {
    desserts: {
      type: Array
    },
  },
  data () {
    return {
      headers: [
        {
          text: '角色',
          align: 'start',
          sortable: false,
          value: 'character',
        },
        { text: '名稱', value: 'name' },
        { text: '總次數', value: 'total' },
        { text: '總機率', value: 'rate' },
      ],
    };
  },
};
</script>

