<template>
  <v-card
      class="pa-2"
      outlined
      tile
      width="82px"
      height="82px"
      :style='getStyle()'
  >
  <div :class="`rarity-${rarity}`" >
    <img
        v-if="attri !== ''"
        :src="`https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/elements/element_${attriMapping[attri]}.png`"
        style="width: 20px; height: 20px;position: absolute; top: 0; right: 0;background-color:white;"
    />
  </div>
  </v-card>
</template>

<script>
export default {
  name: 'CharacterIcon',
  data () {
    return {
      attriMapping: { Fire: 'red', Water: 'blue', Thunder: 'yellow', Wind: 'green', Light: 'white', Dark: 'black' },
      rarityStyle: ['', '', '', 'white', 'gold', 'conic-gradient(#fd004c, #fe9000, #fff020, #3edf4b, #3363ff, #b102b7, #fd004c)'],
    };
  },
  methods: {
    clickButton () {
      this.$emit('click');
    },
    getStyle () {
      let style = {
        'background-image': this.id === '' ? `url("https://lpc.opengameart.org/sites/default/files/TransparencyDark640.png")` : `url("https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/chars/${this.id}/square_0.png")`,
        'border-style': 'solid',
        'border-width': 'thick',
        'background-size': 'contain'
      }

      if(this.rarity === '5'){
        style['border-image-slice'] = 1;
        style['border-image-source'] = "conic-gradient(#fd004c,#fe9000,#fff020,#3edf4b,#3363ff,#b102b7,#fd004c)";
        return style;
      }
      style['border-color'] = this.rarity === '' ? '' :this.rarityStyle[this.rarity];
      return style;
    }
  },
  props: {
    attri: {
      type: String
    },
    id: {
      type: String
    },
    name: {
      type: String
    },
    rarity: {
      type: String
    },
  }
};
</script>

<style lang="scss" scoped>


@mixin rarity {
  background-size: 55px 15px;
  display: inline-block;
  width: 55px;
  height: 15px;
  content: "";
  background-color: #333333;
  position: absolute;
  bottom: -5px;
  left: -5px;
}

.rarity-3::after {
  background-image: url(https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/rarity/star3.png);
  @include rarity;
}

.rarity-4::after {
  background-image: url(https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/rarity/star4.png);
  @include rarity;
}

.rarity-5::after {
  background-image: url(https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/rarity/star5.png);
  @include rarity;
}

.rarity-5-pu::after {
  background-image: url(https://raw.githubusercontent.com/Zhen-Bo/flipper_gacha_simulator/main/static/image/rarity/star5.png);
  @include rarity;
}
</style>


