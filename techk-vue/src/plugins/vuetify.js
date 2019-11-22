import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.green.lighten1,
        secondary: colors.green.lighten4,
        accent: colors.blue.darken1,
        error: colors.red.lighten2,
        info: colors.blue.lighten2,
        success: colors.green.lighten3,
        warning: colors.yellow.lighten2,
      },
    },
  },
});
