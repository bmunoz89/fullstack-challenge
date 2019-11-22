<template>
  <v-container>
    <v-dialog v-model="dialog" max-width="1000">
      <template v-slot:activator="{ on }">
        <a dark v-on="on">{{ book.title }}</a>
      </template>

      <v-card>
        <v-card-title class="headline" v-text="book.title"></v-card-title>
        <v-divider></v-divider>
        <v-row class="col-12">
          <v-col class="col-2">
            <v-img :src="book.thumbnail_url"></v-img>
          </v-col>
          <v-col class="col-10">
            <v-card-subtitle class="text-justify" v-text="book.product_description"></v-card-subtitle>
          </v-col>
        </v-row>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
export default {
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      dialog: false
    };
  }
};
</script>

<style scoped>
a {
  text-decoration: underline;
}
</style>
