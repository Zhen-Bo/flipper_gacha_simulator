<template>
  <div>
    <AppNav>
    </AppNav>
    <v-card class="mt-2" >
      <v-card-text class="pl-0 pr-0">
        <v-data-table
            :headers="headers"
            :items="desserts"
            :items-per-page="-1"
            mobile-breakpoint="0"
            hide-default-footer
        ></v-data-table>
      </v-card-text>
    </v-card>

    <v-card class="mt-2" >
      <v-card-title class="pb-0">最常出現的5星</v-card-title>
      <v-card-text class="pl-0 pr-0">
        <v-data-table
            :headers="headers1"
            :items="desserts1"
            :items-per-page="-1"
            mobile-breakpoint="0"
            hide-default-footer
        >
          <template v-slot:item.character="{ item }">
            <character-icon
                            :attri="item.character.attri"
                            :name="item.character.name"
                            :id="item.character.id"
                            :rarity="item.character.rarity"/>
          </template>

        </v-data-table>
      </v-card-text>

    </v-card>
  </div>
</template>

<script>
import AppNav from '@/components/Nav';
import CharacterIcon from '@/components/CharacterIcon';

export default {
  name: 'Report',
  components: { CharacterIcon, AppNav },
  data () {
    return {
      headers: [
        {
          text: '稀有度',
          align: 'start',
          sortable: false,
          value: 'star',
        },
        { text: '總出貨次數', value: 'all' },
        { text: '總出貨率', value: 'rate' }
      ],
      desserts: [
        { star: '5星', all: '63767', rate: '4.997%' },
        { star: '4星', all: '408508', rate: '32.013%' },
        { star: '3星', all: '803795', rate: '62.990%' },
        { star: '統計', all: '1276070', rate: '100.000%' }
      ],
      headers1: [
        {
          text: '角色',
          align: 'start',
          sortable: false,
          value: 'character',
        },
        { text: '名稱', value: 'name' },
        { text: '總出貨率', value: 'rate' }
      ],
      desserts1: [
        { character: {"name":"水前","id":"onmyoji_boy","attri":"Water","rarity":"5"}, name: '水前', rate: '40%' },
        { character: {"name":"列恩","id":"mercenary","attri":"Wind","rarity":"5"}, name: '風叔', rate: '30%' },
        { character: {"name":"瓦格納","id":"fire_dragon","attri":"Fire","rarity":"5"}, name: '火龍', rate: '20%' },
      ],
    };
  },
};
</script>
