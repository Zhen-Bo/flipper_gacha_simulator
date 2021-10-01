<template>
  <div :class="`character-icon-border-${rarity}`">
    <v-card
        outlined
        tile
        width="82px"
        height="82px"
        :style='getStyle()'
    >
      <div :class="`rarity-${rarity}`">
        <img
            :alt="attri"
            class="character-icon-attri"
            v-if="attri !== ''"
            :src="`${resourceURL}/static/image/elements/element_${attriMapping[attri]}.png`"
        />
      </div>
    </v-card>
  </div>
</template>

<script>
import API from '@/plugins/api';

export default {
  name: 'CharacterIcon',
  data () {
    return {
      resourceURL: API.resourceURL,
      attriMapping: { Fire: 'red', Water: 'blue', Thunder: 'yellow', Wind: 'green', Light: 'white', Dark: 'black' },
    };
  },
  methods: {
    clickButton () {
      this.$emit('click');
    },
    getStyle () {
      let style = {
        'box-shadow': 'rgb(170 170 170 / 35%) 0px 0px 4px 4px inset',
        'background-image': this.id === '' ? `url("https://lpc.opengameart.org/sites/default/files/TransparencyDark640.png")` : `url("${this.resourceURL}/static/image/chars/${this.id}/square_0.png")`,
        'border-style': 'solid',
        'border-width': 'thick',
        'background-size': 'contain',
        'border-radius': '4px'
      };

      if (this.rarity === '5-pu') {
        style['border-image-slice'] = 1;
        style['border-image-source'] = 'conic-gradient(#fd004c,#fe9000,#fff020,#3edf4b,#3363ff,#b102b7,#fd004c)';
        return style;
      }

      style['border-color'] = 'white';
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
  content: "";
  background-color: #343333;
  background-position: center;
  position: absolute;
  bottom: -7px;
  left: -7px;
  border-radius: 0 0 0 4px;
}

.rarity-3::after {
  background-image: url($VUE_APP_RESOURCE_URL +'/static/image/rarity/star3.png');
  width: 35px;
  height: 15px;
  @include rarity;
}

.rarity-4::after {
  background-image: url($VUE_APP_RESOURCE_URL + '/static/image/rarity/star4.png');
  width: 45px;
  height: 15px;
  @include rarity;
}

.rarity-5::after {
  background-image: url($VUE_APP_RESOURCE_URL +'/static/image/rarity/star5.png');
  width: 55px;
  height: 15px;
  @include rarity;
}

.rarity-5-pu::after {
  background-image: url($VUE_APP_RESOURCE_URL + '/static/image/rarity/star5.png');
  width: 55px;
  height: 15px;
  @include rarity;
}

.character-icon-attri {
  width: 20px;
  height: 20px;
  position: absolute;
  top: -1px;
  right: -1px;
  background-color: white;
  margin: 0 0 4px 4px;
  border-style: solid;
  border-width: 2px;
  border-color: white;
  border-radius: 0 0 0 4px;
}

@mixin character-icon-border {
  border-radius: 4px;
  border-style: solid;
  border-width: 2px;
}

.character-icon-border-5, .character-icon-border-5-pu {
  border-image-slice: 1;
  border-image-source: conic-gradient(#fd004c, #fe9000, #fff020, #3edf4b, #3363ff, #b102b7, #fd004c);
  @include character-icon-border;
}

.character-icon-border-, .character-icon-border-4, .character-icon-border-3 {
  border-color: rgb(170, 170, 170);
  @include character-icon-border;
}
</style>


