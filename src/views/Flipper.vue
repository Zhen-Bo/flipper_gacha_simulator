<template>
  <div>
    <v-img :src='`${resourceURL}/static/image/pool_image/${pool}.png`'></v-img>
    <result-card :character-list="result"></result-card>

    <v-img :src='require("..\\assets\\bg.jpg")'>
      <v-container class="justify-center mt-3">
        <v-row class="justify-center mb-3">
          <v-card width="400px" v-if="isRoll">
            <v-card-text class="mb-0 pb-0">此結果為這個網站第 <span style="color: #ffcd76">{{ total }}</span> 次模擬
            </v-card-text>
            <v-card-text>

              <v-data-table
                  :headers="headers"
                  :items="desserts"
                  :items-per-page="-1"
                  mobile-breakpoint="0"
                  hide-default-footer
              >
                <template v-slot:foot>
                  <tr>
                    <td></td>
                    <td></td>
                    <td colspan="2" class="text-right">
                      你已抽取{{ rollTotal }}次
                    </td>
                  </tr>
                </template>
              </v-data-table>

            </v-card-text>
          </v-card>
        </v-row>

        <v-row class="justify-space-around mb-2">
          <v-btn text/>
          <roll-button @click="roll"/>
          <v-btn height="64px">
            <v-icon>
              mdi-share-variant
            </v-icon>
          </v-btn>
        </v-row>
      </v-container>
    </v-img>
  </div>
</template>

<script>
import API from '../plugins/api';
import RollButton from '@/components/RollButton';
import ResultCard from '@/components/ResultCard';

export default {
  name: 'Flipper',
  components: { ResultCard, RollButton },
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
      headers: [
        {
          text: '',
          align: 'start',
          sortable: false,
          value: 'title',
        },
        { text: '5星', value: 'star5', sortable: false, align: 'end' },
        { text: '4星', value: 'star4', sortable: false, align: 'end' },
        { text: '3星', value: 'star3', sortable: false, align: 'end' }
      ],
      desserts: [],
      rollTotal: 0
    };
  },
  methods: {
    roll () {
      API.roll(this.pool).then((rs) => {
        let report = { '3': 0, '4': 0, '5': 0 };
        let count = this.desserts[1] ? this.desserts[1] : { title: '總數目', star5: 0, star4: 0, star3: 0 };

        rs.data.forEach(i => {
          report[i.rarity]++;
        });

        count.star5 += report['5'];
        count.star4 += report['4'];
        count.star3 += report['3'];

        let countTotal = count.star5 + count.star4 + count.star3;
        this.desserts = [
          { title: '本次', star5: report['5'], star4: report['4'], star3: report['3'] },
          count,
          {
            title: '機率',
            star5: `${(Math.round((count.star5 / countTotal) * 10000) / 100).toFixed(2)}%`,
            star4: `${(Math.round((count.star4 / countTotal) * 10000) / 100).toFixed(2)}%`,
            star3: `${(Math.round((count.star3 / countTotal) * 10000) / 100).toFixed(2)}%`
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
