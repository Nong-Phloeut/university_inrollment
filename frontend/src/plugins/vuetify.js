// Vuetify plugin setup
import "vuetify/styles";
import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "@mdi/font/css/materialdesignicons.css";
import * as labsComponents from "vuetify/labs/components";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export default createVuetify({
  components: {
    ...components,
    ...labsComponents,
  },
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: "light",
  },
  defaults: {
    VBtn: {
      color: "primary",     // Default button color
      variant: "flat",      // Default variant (e.g. flat, outlined, text)
      rounded: "md",        // Default rounded corners (xs, sm, md, lg, xl)
    },
  },
});
