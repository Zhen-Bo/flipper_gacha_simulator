<template>
  <v-img
      class="mt-2"
      gradient="to top right, rgba(100,115,201,.33), rgba(25,32,72,.7)"
      :src='`https://tw.hicdn.beanfun.com/beanfun/WebImage/1606509847551.png`'
      height="300px"
      width="440px"
  >
    <v-container class="mt-2">
      <v-row class="justify-center mb-3" v-for="(row, index) in [3, 4, 3]" :key="`row_${index}_${row}`">
        <character-icon v-for="n in row" :key="n"
                        :attri="result[index][n]? result[index][n].attri: ''"
                        :name="result[index][n]? result[index][n].name: ''"
                        :id="result[index][n]? result[index][n].id: ''"
                        :rarity="result[index][n]?result[index][n].rarity:''"/>
      </v-row>
    </v-container>
  </v-img>
</template>

<script>
import CharacterIcon from '@/components/CharacterIcon';

export default {
  name: 'ResultCard',
  components: { CharacterIcon },
  props: {
    characterList: {
      type: Array
    },
  },
  data () {
    return {
      result: [[], [], []]
    };
  },
  methods: {
    clickButton () {
      this.$emit('click');
    },
    /**
     * @param {array<{attri: string, id: string, name: string, rarity:string}>} data
     */
    splitToRow (data) {
      let rollDate = [[], [], []];
      if (!data || data.length !== 10) { return rollDate; }

      data.forEach((i, index) => {
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
      });

      return rollDate;
    }
  },
  watch: {
    characterList (newValue, oldValue) {
      console.log(newValue);
      console.log(oldValue);

      this.result = this.splitToRow(newValue);
    }
  },
};
</script>
