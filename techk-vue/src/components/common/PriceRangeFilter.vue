<template>
  <v-container>
    <div>
      <v-subheader>Price range</v-subheader>
      <v-range-slider v-model="price" :min="min" :max="max" hide-details class="align-center">
        <template v-slot:prepend>
          <v-text-field
            v-model="price[0]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
          ></v-text-field>
        </template>
        <template v-slot:append>
          <v-text-field
            v-model="price[1]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
          ></v-text-field>
        </template>
      </v-range-slider>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "PriceRangeFilter",
  data() {
    return {
      min: 0,
      max: 100,
      price: [0, 100]
    };
  },
  watch: {
    price(value) {
      this.$store.commit("updatePriceGTFilter", value[0]);
      this.$store.commit("updatePriceLTFilter", value[1]);
    },
    deep: true
  }
};
</script>
