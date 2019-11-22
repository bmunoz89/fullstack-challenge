<template>
  <v-container>
    <div>
      <v-text-field v-model="saveProductDescription" label="Product description"></v-text-field>
    </div>
  </v-container>
</template>


<script>
export default {
  name: "ProductDescriptionFilter",
  computed: {
    saveProductDescription: {
      get() {
        return this.$store.state.filters_product_description;
      },
      set(value) {
        this.$store.commit("updateProductDescriptionFilter", value);
      }
    }
  }
};
</script>
