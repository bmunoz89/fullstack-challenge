<template>
  <v-container>
    <div>
      <v-text-field v-model="saveTitle" label="Title"></v-text-field>
    </div>
  </v-container>
</template>


<script>
export default {
  name: "TitleFilter",
  computed: {
    saveTitle: {
      get() {
        return this.$store.state.filters_title;
      },
      set(value) {
        this.$store.commit("updateTitleFilter", value);
      }
    }
  }
};
</script>
