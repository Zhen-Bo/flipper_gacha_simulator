<template>
  <div>
    <v-card class="mt-2">
      <v-card-text class="pl-0 pr-0">
        <star-report :desserts="rollDesserts" :five-pu="false"></star-report>
      </v-card-text>
    </v-card>

    <v-card class="mt-2">
      <v-card-title class="pb-0">角色出貸統計</v-card-title>
      <v-card-text class="pl-0 pr-0">
        <v-tabs
            v-model="tab"
            color="#fb8c00"
            centered
        >
          <v-tab
              v-for="item in tabItems"
              :key="item.name"
          >
            {{ item.text }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item
              v-for="item in tabItems"
              :key="item.name"
          >
            <v-card flat>
              <character-report :desserts="characterReportList[item.name]"/>
            </v-card>
          </v-tab-item>
        </v-tabs-items>


      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import API from '@/plugins/api';
import StarReport from '@/components/StarReport';
import CharacterReport from '@/components/CharacterReport';

export default {
  name: 'Report',
  components: { CharacterReport, StarReport },
  props: {
    pool: {
      type: String,
      default: ''
    },
  },
  data () {
    return {
      rollDesserts: [],
      lastUpdateTime: '',
      characterReportList: [[], [], [], [], [], []],
      tab: 5,
      tabItems: [{ name: 5, text: '5 星' }, { name: 4, text: '4 星' }, { name: 3, text: '5 星' }]
    };
  },
  methods: {
    /** @param {array<character & {total:number}>} list */
    countRate (list) {
      let total = list.map(rs => rs.total).reduce((a, b) => a + b);
      list.forEach((rs) => {
        rs.rate = `${API.round(rs.total / total)}%`;
      });
      return list;
    }
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

    API.getCharacterReport(this.pool).then((rs) => {
      this.lastUpdateTime = new Date(rs.last_run_time);
      this.characterReportList = [[], [], [],
        this.countRate(rs.report.filter(rs => rs.rarity === '3')),
        this.countRate(rs.report.filter(rs => rs.rarity === '4')),
        this.countRate(rs.report.filter(rs => rs.rarity === '5' || rs.rarity === '5-pu'))];
    });
  }
};
</script>
