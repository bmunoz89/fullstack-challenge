<template>
  <v-container>
    <div>
      <v-switch v-model="saveStock" label="Stock"></v-switch>
    </div>
  </v-container>
</template>

<script>
export default {
  name: "StockFilter",
  computed: {
    saveStock: {
      get() {
        return this.$store.state.filters_stock;
      },
      set(value) {
        this.$store.commit("updateStockFilter", value);
      }
    }
  }
};
</script>
