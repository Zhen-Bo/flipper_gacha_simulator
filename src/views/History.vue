<template>
  <div class="grey lighten-4">
    <v-sheet color="primary" class="pa-2">
      <v-text-field
          v-model="searchNumber"
          label="模擬結果查詢"
          placeholder="模擬結果查詢"
          solo
          dark
          dense
          inputmode="numeric"
          hide-details
          append-icon="mdi-magnify"
          filled
          solo-inverted
          @click:append="search"
          @keydown.enter="search"
      ></v-text-field>
    </v-sheet>

    <v-card class="mt-2" v-if="searchRS.data.length > 0">
      <v-card-title class="pb-1">第{{ searchNumberRS }}次記錄
      </v-card-title>
      <v-card-text class="pl-0 pr-0 mt-0">
        <result-card :style="`zoom:${zoom}`" :character-list="searchRS.data"></result-card>
      </v-card-text>
    </v-card>

    <v-card class="mt-2">
      <v-card-title>你的最近{{ total }}個記錄
        <v-spacer/>
        <tooltip-icon-button icon="mdi-delete" message="刪除記錄" @click="deleteHistory"/>
      </v-card-title>
      <v-card-text class="pl-0 pr-0">
        <star-report :desserts="reportDesserts"/>
        <v-divider/>
        <v-timeline
            align-top
            dense
            v-if="total > 0"
        >
          <v-timeline-item
              v-for="item in items" :key="item.dateTime"
              :color="dotColor[getTopStar(item.data)]"
              :small="getTopStar(item.data) !== '5-pu'"
          >
            <strong>{{ item.dateTime  | moment('MMMM Do YYYY, h:mm:ss a') }}</strong>
            <result-card :style="`zoom:${0.8 * zoom}`" :character-list="item.data"></result-card>
          </v-timeline-item>
        </v-timeline>

      </v-card-text>
    </v-card>

  </div>
</template>

<script>
import API from '@/plugins/api';
import ResultCard from '@/components/ResultCard';
import StarReport from '@/components/StarReport';
import TooltipIconButton from '@/components/TooltipIconButton';

export default {
  name: 'History',
  components: { TooltipIconButton, StarReport, ResultCard },
  data () {
    return {
      total: 0,
      /** @type {array<{data:array<character>,  dateTime:string}>} */
      items: [],
      reportDesserts: [],
      dotColor: { '5-pu': 'red darken-3', '5': 'red lighten-2', '4': 'orange lighten-2', '3': 'white' },
      zoom: API.getZoom(this.$vuetify.breakpoint.width),
      searchNumber: '',
      searchNumberRS: '',
      searchRS: { data: [] }
    };
  },
  props: {
    pool: {
      type: String,
      default: ''
    },
  },
  methods: {
    search () {
      API.search(this.pool, this.searchNumber)
          .then((rs) => {
            this.searchRS.data = rs.data;
            this.searchNumberRS = this.searchNumber;
          })
          .catch((rs) => {
            this.searchRS.data = [];
            this.searchNumberRS = 0;
            this.$root.$snackbar.Show(rs.message, 'error');
          });
    },
    deleteHistory () {
      localStorage.removeItem(this.pool);
      this.loadLocalStorage();
    },
    /** @param {array<character>} characterList */
    getTopStar (characterList) {
      let top = 0;
      for (let i = 0; i < characterList.length; i++) {
        let rs = characterList[i];
        switch (rs.rarity) {
          case '5-pu':
            return '5-pu';
          case '5':
            if (top < 5) { top = 5;}
            break;
          case '4':
            if (top < 4) { top = 4;}
            break;
          case '3':
            if (top < 3) { top = 3;}
            break;
        }
      }
      return '' + top;
    },
    updateReport () {
      let count = { title: '總數目', star5_up: 0, star5: 0, star4: 0, star3: 0 };
      let countTotal = 0;

      this.items.forEach((rs) => {
        countTotal++;

        rs.data.forEach((ch) => {
          switch (ch.rarity) {
            case '5-pu':
              count.star5_up++;
              break;
            case '5':
              count.star5++;
              break;
            case '4':
              count.star4++;
              break;
            case '3':
              count.star3++;
              break;
          }
        });
      });

      this.reportDesserts = [
        count,
        {
          title: '機率',
          star5_up: `${(Math.round((count.star5_up / (countTotal * 10)) * 10000) / 100).toFixed(2)}%`,
          star5: `${(Math.round((count.star5 / (countTotal * 10)) * 10000) / 100).toFixed(2)}%`,
          star4: `${(Math.round((count.star4 / (countTotal * 10)) * 10000) / 100).toFixed(2)}%`,
          star3: `${(Math.round((count.star3 / (countTotal * 10)) * 10000) / 100).toFixed(2)}%`
        }
      ];
    },
    clear () {
      this.total = 0;
      this.items = [];
      this.reportDesserts = [
        { title: '總數目', star5_up: 0, star5: 0, star4: 0, star3: 0 },
        { title: '機率', star5_up: '0.00%', star5: '0.00%', star4: '0.00%', star3: '0.00%' }
      ];
    },
    loadLocalStorage () {
      let item = localStorage.getItem(this.pool);
      if (!item) {
        this.clear();
        return;
      }

      this.items = JSON.parse(item);
      this.total = this.items.length;
      this.updateReport();
    }
  },
  created () {
    this.loadLocalStorage();
  }
};
</script>
