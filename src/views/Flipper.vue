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
                  <v-simple-table>
                    <template v-slot:default>
                      <thead>
                      <tr>
                        <th class="text-center">5星</th>
                        <th class="text-center">3星</th>
                        <th class="text-center">2星</th>
                      </tr>
                      </thead>
                      <tbody>
                      <tr>
                        <td class="text-center">{{ resultReport[0] }}</td>
                        <td class="text-center">{{ resultReport[1] }}</td>
                        <td class="text-center">{{ resultReport[2] }}</td>
                      </tr>
                      </tbody>
                    </template>
                  </v-simple-table>

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
      resultReport: [0, 0, 0],
      total: 0
    };
  },
  methods: {
    roll () {
      API.roll(this.pool).then((rs) => {
        let report = { '3': 0, '4': 0, '5': 0 };

        rs.data.forEach(i => {
          report[i.rarity]++;
        });

        this.total = rs.total;
        this.resultReport = [report['5'], report['4'], report['3']];
        this.result = rs.data;
        this.isRoll = true;
      });
    }
  }
};
</script>
