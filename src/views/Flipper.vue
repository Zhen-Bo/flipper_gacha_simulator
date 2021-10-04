<template>
  <v-card>
    <v-img :src='`${resourceURL}/static/image/pool_image/${pool}.png`' max-width="600px"
           :height="$vuetify.breakpoint.width / 1.9"
           max-height="315px"
           :load="load = false">
      <template v-slot:placeholder>
        <v-sheet>
          <v-skeleton-loader
              class="mx-auto"
              :height="$vuetify.breakpoint.width / 1.9"
              type="image"
          ></v-skeleton-loader>
        </v-sheet>
      </template>
    </v-img>

    <result-card :character-list="result" :style="`zoom:${zoom}`"></result-card>

    <v-img :src='require("..\\assets\\bg.jpg")'>
      <v-container class="justify-center mt-3">

        <v-row class="justify-space-around mb-2">
<!--          <v-btn text/>-->
          <roll-button @click="roll"/>
<!--          <v-btn height="64px">-->
<!--            <v-icon>-->
<!--              mdi-share-variant-->
<!--            </v-icon>-->
<!--          </v-btn>-->
        </v-row>

        <v-row class="justify-center mb-3">
          <v-card max-width="600px"  width="100%" v-if="isRoll">
            <v-card-text class="mb-0 pb-0">此結果為這個網站第 <span style="color: #ffcd76">{{ total }}</span> 次模擬
            </v-card-text>
            <v-card-text>
              <star-report :desserts="desserts" :roll-total="rollTotal"/>
            </v-card-text>
          </v-card>
        </v-row>
      </v-container>
    </v-img>
  </v-card>
</template>

<script>
import API from '../plugins/api';
import RollButton from '@/components/RollButton';
import ResultCard from '@/components/ResultCard';
import StarReport from '@/components/StarReport';

export default {
  name: 'Flipper',
  components: { StarReport, ResultCard, RollButton },
  props: {
    pool: {
      type: String,
      default: ''
    },
  },
  data () {
    return {
      resourceURL: API.resourceURL,
      isRoll: false,
      result: [],
      total: 0,
      desserts: [],
      rollTotal: 0,
      zoom: API.getZoom(this.$vuetify.breakpoint.width),
      load: true
    };
  },
  methods: {
    roll () {
      API.roll(this.pool).then((rs) => {
        let report = { '3': 0, '4': 0, '5': 0, '5-pu': 0 };
        let count = this.desserts[1] ? this.desserts[1] : { title: '總數目', star5_up: 0, star5: 0, star4: 0, star3: 0 };

        rs.data.forEach(i => {
          report[i.rarity]++;
        });

        count.star5_up += report['5-pu'];
        count.star5 += report['5'];
        count.star4 += report['4'];
        count.star3 += report['3'];

        let countTotal = count.star5_up + count.star5 + count.star4 + count.star3;
        this.desserts = [
          { title: '本次', star5_up: report['5-pu'], star5: report['5'], star4: report['4'], star3: report['3'] },
          count,
          {
            title: '機率',
            star5_up: `${API.round(count.star5_up / countTotal)}%`,
            star5: `${API.round(count.star5 / countTotal)}%`,
            star4: `${API.round(count.star4 / countTotal)}%`,
            star3: `${API.round(count.star3 / countTotal)}%`
          },
        ];

        this.total = rs.total;
        this.rollTotal++;
        this.result = rs.data;
        this.isRoll = true;

        this.saveHistory(rs.data);
      });
    },
    saveHistory (data) {
      let key = this.pool;
      let history = localStorage.getItem(key);

      if (!history) {
        localStorage.setItem(key, JSON.stringify([]));
        history = [];
      } else {
        history = JSON.parse(history);
      }

      history.unshift({ data, dateTime: new Date() });

      if (history.length > 10) {
        history.pop();
      }
      localStorage.setItem(key, JSON.stringify(history));
    }
  }
};
</script>

<style lang="scss" scoped>
::v-deep .v-skeleton-loader.v-skeleton-loader--is-loading {
  .v-skeleton-loader__image {
    height: 100%;
  }
}
</style>
