import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    filters_title: '',
    filters_product_description: '',
    filters_price__gt: '',
    filters_price__lt: '',
    filters_stock: true,
    filters_category: '',
    table_loading: true,
    table_books: [],
    table_totalBooks: 0,
    table_options: {}
  },
  mutations: {
    updateTitleFilter(state, value) {
      state.filters_title = value;
    },
    updateProductDescriptionFilter(state, value) {
      state.filters_product_description = value;
    },
    updatePriceGTFilter(state, value) {
      state.filters_price__gt = value;
    },
    updatePriceLTFilter(state, value) {
      state.filters_price__lt = value;
    },
    updateStockFilter(state, value) {
      state.filters_stock = value;
    },
    updateCategoryFilter(state, value) {
      state.filters_category = value;
    },
    updateTableLoading(state, value) {
      state.table_loading = value;
    },
    updateTableBooks(state, value) {
      state.table_books = value;
    },
    updateTableTotalBooks(state, value) {
      state.table_totalBooks = value;
    },
    updateTableOptions(state, value) {
      state.table_options = value;
    }
  },
  actions: {
    async filterTable({ commit, state }) {
      commit('updateTableLoading', true);

      const { page, itemsPerPage } = state.table_options;
      let url = 'http://localhost:8000/book/'
      url += `?limit=${itemsPerPage}`
      url += `&offset=${(page - 1) * itemsPerPage}`;

      if (state.filters_title)
        url += `&title=${state.filters_title}`;
      if (state.filters_product_description)
        url += `&product_description=${state.filters_product_description}`;
      if (state.filters_price__lt)
        url += `&price__lt=${state.filters_price__lt}`;
      if (state.filters_price__gt)
        url += `&price__gt=${state.filters_price__gt}`;
      url += `&stock=${state.filters_stock}`;
      if (state.filters_category)
        url += `&category=${state.filters_category}`;

      try {
        const response = await axios.get(url);
        commit('updateTableBooks', response.data["results"]);
        commit('updateTableTotalBooks', response.data["count"]);
        commit('updateTableLoading', false);
      }
      catch (e) {
        return commit('updateTableLoading', false);
      }
    },
    async deleteBook({ state }, item) {
      const index = state.table_books.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        state.table_books.splice(index, 1);

      await axios.delete(`http://localhost:8000/book/${item.id}/`);
    }
  },
  modules: {
  }
})
