<template>
  <v-container>
    <div>
      <TitleFilter />
      <ProductDescriptionFilter />
      <CategoryFilter />
      <PriceRangeFilter />
      <v-container>
        <v-row no-gutters>
          <v-col cols="6" no-gutters>
            <StockFilter />
          </v-col>
          <v-col cols="6" no-gutters>
            <v-btn color="primary" v-on:click="filterTable">Filter</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-container>
</template>

<script>
import TitleFilter from "./common/TitleFilter";
import ProductDescriptionFilter from "./common/ProductDescriptionFilter";
import CategoryFilter from "./common/CategoryFilter";
import StockFilter from "./common/StockFilter";
import PriceRangeFilter from "./common/PriceRangeFilter";

export default {
  name: "Filters",
  components: {
    TitleFilter,
    ProductDescriptionFilter,
    CategoryFilter,
    StockFilter,
    PriceRangeFilter
  },
  methods: {
    filterTable() {
      this.$store.dispatch("filterTable");
    }
  }
};
</script>
