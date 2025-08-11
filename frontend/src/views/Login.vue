<template>
  <v-container
    fluid
    class="fill-height d-flex align-center justify-center pa-8"
  >
    <v-row
      class="elevation- rounded-lg"
      style="background-color: white"
      no-gutters
    >
      <!-- Left: image -->
      <v-col cols="12" md="8" class="d-flex align-center justify-center pa-8">
        <v-img
          src="https://www.shutterstock.com/image-vector/set-happy-graduation-people-wearing-600nw-1958315083.jpg"
          alt="Login Illustration"
          max-width="100%"
          height="auto"
          cover
        />
      </v-col>
      <!-- Right: login form -->
      <v-col cols="12" md="4" class="pa-10">
        <v-card flat>
          <v-card-title class="mb-4 pa-0">
            Welcome to Pharmacy University
          </v-card-title>

          <v-form ref="form" @submit.prevent="handleLogin">
            <div
              class="text-medium-emphasis d-flex align-center justify-space-between"
            >
              Email
            </div>
            <v-text-field
              placeholder="Email"
              ref="emailField"
              prepend-inner-icon="mdi-email-outline"
              v-model="email"
              :rules="emailRules"
              variant="outlined"
              no-validation
              :error-messages="incorrect"
              color="textField"
              autocomplete="username"
            ></v-text-field>
            <div
              class="text-medium-emphasis d-flex align-center justify-space-between"
            >
              Password

              <router-link
                class="text-decoration-none text-blue"
                to="forgot-password"
                rel="noopener noreferrer"
                target="_black"
              >
                Forget password?
              </router-link>
            </div>
            <v-text-field
              placeholder="Password"
              :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible ? 'text' : 'password'"
              prepend-inner-icon="mdi-lock-outline"
              v-model="password"
              :rules="passwordRules"
              variant="outlined"
              @click:append-inner="visible = !visible"
              :error-messages="incorrect"
              color="textField"
              autocomplete="new-password"
            ></v-text-field>

            <v-checkbox label="Remember me" density="compact" class="mb-4" />

            <v-btn
              type="submit"
              color="primary darken-4 mt-7"
              block
              size="large"
              class="login-button"
            >
              Login
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/userStore";

const router = useRouter();
const userStore = useUserStore();

const email = ref("");
const password = ref("");
const form = ref(null);
const loading = ref(false);

const emailRules = [
  (v) => !!v || "E-mail is required",
  (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
];

const passwordRules = [
  (v) => !!v || "Password is required",
  (v) => (v && v.length >= 8) || "Password must be at least 8 characters",
];

async function handleLogin() {
  const isValid = await form.value?.validate();
  if (!isValid) return;

  loading.value = true;
  userStore.error = null;

  try {
    await userStore.connection({
      username: email.value,
      password: password.value,
    });
    router.push("/dashboard");
  } catch {
    // error is handled inside the store
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
}
</style>
