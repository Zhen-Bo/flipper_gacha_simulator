<template>
  <div>
    <v-card class="mt-2">
      <v-card-text class="pl-0 pr-0">
        <star-report :desserts="rollDesserts" :five-pu="false"></star-report>
      </v-card-text>
    </v-card>

    <v-card class="mt-2">
      <v-card-title class="pb-0">最常出現的5星</v-card-title>
      <v-card-text class="pl-0 pr-0">
        <v-data-table
            :headers="headers1"
            :items="desserts1"
            :items-per-page="-1"
            mobile-breakpoint="0"
            hide-default-footer
        >
          <template v-slot:item.character="{ item }">
            <character-icon
                :attri="item.character.attri"
                :name="item.character.name"
                :id="item.character.id"
                :rarity="item.character.rarity"/>
          </template>

        </v-data-table>
      </v-card-text>

    </v-card>
  </div>
</template>

<script>
import API from '@/plugins/api';
import CharacterIcon from '@/components/CharacterIcon';
import StarReport from '@/components/StarReport';

export default {
  name: 'Report',
  components: { StarReport, CharacterIcon },
  props: {
    pool: {
      type: String,
      default: ''
    },
  },
  data () {
    return {
      rollDesserts:[],
      headers1: [
        {
          text: '角色',
          align: 'start',
          sortable: false,
          value: 'character',
        },
        { text: '名稱', value: 'name' },
        { text: '總出貨率', value: 'rate' }
      ],
      desserts1: [
        { character: { 'name': '水前', 'id': 'onmyoji_boy', 'attri': 'Water', 'rarity': '5' }, name: '水前', rate: '40%' },
        { character: { 'name': '列恩', 'id': 'mercenary', 'attri': 'Wind', 'rarity': '5' }, name: '風叔', rate: '30%' },
        { character: { 'name': '瓦格納', 'id': 'fire_dragon', 'attri': 'Fire', 'rarity': '5' }, name: '火龍', rate: '20%' },
      ],
    };
  },
  created () {
    API.report(this.pool).then((rs) => {
      this.rollDesserts = [
        { title: '總出貸次數', star5_up: '0', star5: rs.all_five, star4: rs.all_four, star3: rs.all_three },
        {
          title: '總出貸機率',
          star5_up: '0',
          star5: `${API.round(rs.all_five / rs.all_roll)}%`,
          star4: `${API.round(rs.all_four / rs.all_roll)}%`,
          star3: `${API.round(rs.all_three / rs.all_roll)}%`
        },
      ];
      console.log(this.rollDesserts);
    });
  }
};
</script>
