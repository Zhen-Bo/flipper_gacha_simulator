<template>
  <div>
    <v-toolbar
        color="primary"
        dark
        flat
    >
      <v-toolbar-title>彈射抽卡模擬</v-toolbar-title>

      <v-spacer></v-spacer>
            <v-btn icon href="https://github.com/Zhen-Bo/flipper_gacha_simulator/issues" target="_blank" >
              <v-icon>mdi-bug</v-icon>
            </v-btn>

      <template v-slot:extension>
        <v-tabs
            v-model="tab"
            align-with-title
        >
          <v-tabs-slider color="yellow"></v-tabs-slider>

          <v-tab
              v-for="item in items"
              :key="item.name"
          >
            {{ item.text }}
          </v-tab>
        </v-tabs>
      </template>
    </v-toolbar>
    <v-tabs-items v-model="tab">
      <v-tab-item
          v-for="item in items"
          :key="item.name"
      >
        <v-img
            :src='`https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/pool_image/${item.name}.png`'
        >
        </v-img>

        <v-img
            class="mt-2"
            gradient="to top right, rgba(100,115,201,.33), rgba(25,32,72,.7)"
            :src='`https://tw.hicdn.beanfun.com/beanfun/WebImage/1606509847551.png`'
            height="300px"
            width="440px"
        >
          <v-container class="mt-2">
            <v-row class="justify-center mb-3" v-for="(row, index) in [3, 4, 3]" :key="`row_${item.name}_${row}`">
              <character-icon v-for="n in row" :key="n"
                              :attri="result[index][n]? result[index][n].attri: ''"
                              :name="result[index][n]? result[index][n].name: ''"
                              :id="result[index][n]? result[index][n].id: ''"
                              :rarity="result[index][n]?result[index][n].rarity:''"/>
            </v-row>
          </v-container>
        </v-img>

        <v-img :src='require("..\\assets\\bg.jpg")'>
          <v-container class="justify-center mt-3">
            <v-row class="justify-center mb-3">
              <v-card width="400px" v-if="isRoll[tab]">
                <v-card-text class="mb-0 pb-0">此結果為這個網站第 <span style="color: #ffcd76">{{ total }}</span> 次模擬</v-card-text>
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


            <v-row class="justify-space-around mb-2" >
              <v-btn text>

              </v-btn>
              <roll-button @click="roll"/>
              <v-btn height="64px">
                <v-icon>
                  mdi-share-variant
                </v-icon>
              </v-btn>
            </v-row>
          </v-container>
        </v-img>

      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>

import RollButton from '@/components/RollButton';
import CharacterIcon from '@/components/CharacterIcon';

export default {
  name: 'Flipper',
  components: { CharacterIcon, RollButton },
  data () {
    return {
      tab: null,
      items: [
        { name: 'machine_police_girl', text: '警察池' }, { name: 'halfanv', text: '半周年禮黑' }
      ],
      isRoll:[false, false],
      text: 'Lorem ipsum dolor ',
      result: [[], [], []],
      resultReport: [0, 0, 0],
      total: 0
    };
  },
  methods: {
    roll () {
      //TODO call api
      // fetch(`wf/roll?pool=machine_police_girl`)
      //     .then(res => {res.json();})
      //     .then(rs =>{
      //       console.log(rs);
      //     });

      let rs = [{ 'attri': 'Wind', 'id': 'tengu_girl', 'name': '琥羽', 'rarity': '4' }, {
        'attri': 'Fire',
        'id': 'half_oni_boy',
        'name': '明日切丸',
        'rarity': '4'
      }, { 'attri': 'Wind', 'id': 'highlander', 'name': '艾凡', 'rarity': '3' }, {
        'attri': 'Wind',
        'id': 'birdman',
        'name': '奧羅爾',
        'rarity': '4'
      }, { 'attri': 'Fire', 'id': 'pirates_girl', 'name': '瑪麗娜', 'rarity': '5' }, {
        'attri': 'Wind',
        'id': 'tiger_treasure_hunter',
        'name': '咪亞',
        'rarity': '4'
      }, { 'attri': 'Fire', 'id': 'tradition_healer', 'name': '哈里莎', 'rarity': '3' }, {
        'attri': 'Water',
        'id': 'hard_face_soldier',
        'name': '瓦魯達',
        'rarity': '3'
      }, { 'attri': 'Thunder', 'id': 'outlaw_panther', 'name': '黑', 'rarity': '3' }, {
        'attri': 'Light',
        'id': 'unicorn_lancer',
        'name': '傑拉爾',
        'rarity': '4'
      }, { '3星': 4, '4星': 5, '5星': 1 }, 126494, {
        'all_five': 63216,
        'all_four': 405020,
        'all_roll': 1264940,
        'all_three': 796704
      }];
      let rollDate = [[], [], []];

      rs.forEach((i, index) => {
        if (i.attri) {
          switch (true) {
            case index < 3:
              rollDate[0][index + 1] = i;
              break;
            case index < 7:
              rollDate[1][index - 2] = i;
              break;
            case index < 10:
              rollDate[2][index - 6] = i;
              break;
            default:
              //TODO Error;
              break;
          }
          this.result = rollDate;
          return;
        }

        if (i['3星']) {
          this.resultReport = [i['3星'], i['4星'], i['5星']];
        }

        if(!isNaN(i)){
          this.total = i;
        }

      });

      this.isRoll[this.tab] = true;
    }
  },
};
</script>
