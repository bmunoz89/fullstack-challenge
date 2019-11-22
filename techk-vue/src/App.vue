<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <h2>Techk: Fullstack challenge</h2>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
      <v-layout text-center wrap>
        <v-row class="col-12" justify="center" no-gutters>
          <v-col class="col-2">
            <div class="display-1">Filters</div>
            <Filters />
          </v-col>
          <v-col class="col-8">
            <div class="display-1">Books</div>
            <ScrapeBooksButton />
            <Books />
          </v-col>
        </v-row>
      </v-layout>
    </v-content>
    <v-footer color="primary" dark>
      <v-spacer></v-spacer>
      <div>&copy; {{ new Date().getFullYear() }}</div>
    </v-footer>
  </v-app>
</template>

<script>
import Filters from "./components/Filters";
import ScrapeBooksButton from "./components/ScrapeBooksButton";
import Books from "./components/Books";

export default {
  name: "App",
  components: {
    Filters,
    ScrapeBooksButton,
    Books
  }
};
</script>
