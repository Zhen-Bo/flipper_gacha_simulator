<template>
    <v-container class="mt-2 resultCard pa-1">

      <v-row justify="center" :class="index === 0 ? 'mb-2 mt-1' : 'mb-2'"
             v-for="(row, index) in [3, 4, 3]" :key="`row_${index}_${row}`">

         <character-icon v-for="(n, row1) in row" :key="n"
                          :class="row1 === 0 ? 'ml-0' : 'ml-3' "
                          :attri="result[index][n]? result[index][n].attri: ''"
                          :name="result[index][n]? result[index][n].name: ''"
                          :id="result[index][n]? result[index][n].id: ''"
                          :rarity="result[index][n]?result[index][n].rarity:''"/>
      </v-row>
    </v-container>
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
      result: this.splitToRow(this.characterList)
    };
  },
  methods: {
    clickButton () {
      this.$emit('click');
    },
    /**
     * @param {array<character>} data
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
    characterList (newValue) {
      this.result = this.splitToRow(newValue);
    }
  },
};
</script>

<style>
.resultCard{
  background-size: cover;
  background-position: center;
  background-image: repeating-linear-gradient(#d6d8dca8,#d6d8dca8),
  repeating-conic-gradient(
      hsla(0, 0%, 100%, 0.51) 0deg 15deg,
      hsla(0,0%,100%,0) 0deg 30deg
  ),
  url("https://tw.hicdn.beanfun.com/beanfun/WebImage/1606509847551.png");
}
</style>
