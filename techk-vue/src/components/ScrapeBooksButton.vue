<template>
  <v-container>
    <div id="scraper-container">
      <v-btn :loading="loading" color="primary" v-on:click="onClick">
        <span>Scrape books</span>
        <v-icon right>mdi-cached</v-icon>
      </v-btn>
    </div>
    <v-alert type="success" v-if="success">{{successMessage}}</v-alert>
    <v-alert type="error" v-if="error">{{errorMessage}}</v-alert>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "ScrapeBooksButton",
  data() {
    return {
      loading: false,
      success: false,
      successMessage: "",
      error: false,
      errorMessage: ""
    };
  },
  methods: {
    onClick() {
      this.success = false;
      this.successMessage = "";
      this.error = false;
      this.errorMessage = "";
      this.loading = true;
      axios
        .post("http://localhost:8000/scraper/")
        .then(response => {
          if (response.data["status"] == "ok") {
            this.success = true;
            const categoryStats = response.data["categories_stats"],
              booksStats = response.data["books_stats"];
            let message = "";
            message += `Categories(Inserted: ${categoryStats["inserted"]},`;
            message += ` Updated: ${categoryStats["updated"]},`;
            message += ` Deleted: ${categoryStats["deleted"]})`;
            message += ` - Books(Inserted ${booksStats["inserted"]})`;
            message += ` Updated: ${booksStats["updated"]},`;
            message += ` Deleted: ${booksStats["deleted"]})`;
            this.successMessage = message;
            this.$store.dispatch("filterTable");
          } else {
            this.error = true;
            this.errorMessage = "Try again";
          }
        })
        .catch(error => {
          this.error = true;
          this.errorMessage = error.message;
        })
        .finally(() => (this.loading = false));
    }
  }
};
</script>

<style scoped>
#scraper-container {
  text-align: right;
  margin-bottom: 10px;
}
</style>
