<template>
  <v-container>
    <div>
      <v-autocomplete
        v-model="saveCategory"
        label="Categories"
        :items="categories"
        :loading="loading"
        :error="error"
        :error-messages="errorMessage"
        cache-items
        clearable
        :auto-select-first="true"
      ></v-autocomplete>
    </div>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "CategoryFilter",
  data() {
    return {
      categories: [],
      loading: true,
      error: false,
      errorMessage: ""
    };
  },
  computed: {
    saveCategory: {
      get() {
        return this.$store.state.filters_category;
      },
      set(value) {
        if (!value) value = "";
        this.$store.commit("updateCategoryFilter", value);
      }
    }
  },
  mounted() {
    axios
      .get("http://localhost:8000/category/")
      .then(response => {
        this.categories = response.data.map(category => {
          return category["name"];
        });
      })
      .catch(() => {
        this.error = true;
        this.errorMessage = "Something went wrong, try to reload";
      })
      .finally(() => (this.loading = false));
  }
};
</script>
