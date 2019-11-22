<template>
  <v-container>
    <div>
      <v-data-table
        :headers="headers"
        :items="table_books"
        :options.sync="options"
        :server-items-length="table_totalBooks"
        :loading="table_loading"
        class="elevation-1"
      >
        <template v-slot:item.title="{ item }">
          <BookDialog :book="item" />
        </template>
        <template v-slot:item.price="{ item }">£ {{ item.price }}</template>
        <template v-slot:item.stock="{ item }">
          <v-icon v-if="item.stock" color="green darken-1" left ligth>mdi-thumb-up</v-icon>
          <v-icon v-else color="red darken-1" left ligth>mdi-thumb-down</v-icon>
        </template>
        <template v-slot:item.action="{ item }">
          <v-btn small @click="deleteBook(item)" color="error darken-1">Delete</v-btn>
        </template>
      </v-data-table>
    </div>
  </v-container>
</template>

<script>
import BookDialog from "./common/BookDialog";
import { mapState } from "vuex";

export default {
  name: "Books",
  components: {
    BookDialog
  },
  data() {
    return {
      headers: [
        {
          text: "Title",
          align: "left",
          sortable: false,
          value: "title"
        },
        {
          text: "Price",
          align: "left",
          sortable: false,
          value: "price"
        },
        {
          text: "Stock",
          align: "left",
          sortable: false,
          value: "stock"
        },
        {
          text: "UPC",
          align: "left",
          sortable: false,
          value: "upc"
        },
        {
          text: "Actions",
          value: "action",
          sortable: false
        }
      ]
    };
  },
  computed: {
    options: {
      get() {
        return this.$store.state.table_options;
      },
      set(value) {
        this.$store.commit("updateTableOptions", value);
      }
    },
    ...mapState(["table_loading", "table_books", "table_totalBooks"])
  },
  watch: {
    options: {
      async handler() {
        await this.$store.dispatch("filterTable");
      }
    },
    deep: true
  },
  async mounted() {
    await this.$store.dispatch("filterTable");
  },
  methods: {
    async deleteBook(item) {
      await this.$store.dispatch("deleteBook", item);
    }
  }
};
</script>
