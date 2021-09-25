<template>
  <div class="grey lighten-4">
    <AppNav/>
    <v-container class="grey lighten-4">
      <v-row>
        <v-text-field
            label="模擬結果查詢"
            placeholder="模擬結果查詢"
            solo
            dense
            hide-details
            append-icon="mdi-magnify"
        ></v-text-field>
      </v-row>
    </v-container>


    <v-card class=" mt-2" >
      <v-card-title>你的最近10個記錄</v-card-title>
      <v-card-text>
        <v-sheet
            v-for="n in 10"
            :key="n"
        >
          <v-skeleton-loader
              class="mx-auto"
              type="card"
          ></v-skeleton-loader>
        </v-sheet>

      </v-card-text>
    </v-card>

  </div>
</template>

<script>
import AppNav from '@/components/Nav';

export default {
  name: 'History',
  components: { AppNav },
  data () {
    return {
      items: [
        { name: 'machine_police_girl', text: '警察池' }, { name: 'halfanv', text: '半周年禮黑' }
      ]
    };
  },
};
</script>
