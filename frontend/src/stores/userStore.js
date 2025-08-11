import { defineStore } from "pinia";
import * as userAPI from "../api/userAPI";

export const useUserStore = defineStore("user", {
  state: () => ({
    users: [],
    loading: false,
    error: null,
  }),

  actions: {
    async fetchUsers() {
      const response = await userAPI.fetchAllUsers();
      this.users = response.data;
    },

    async createUser(user) {
      try {
        await axios.post("http://localhost:5000/users", user);
        await this.fetchUsers();
      } catch (error) {
        this.error = error.response?.data || "Failed to create user";
      }
    },

    async updateUser(id, updatedUser) {
      try {
        await axios.put(`http://localhost:5000/users/${id}`, updatedUser);
        await this.fetchUsers();
      } catch (error) {
        this.error = error.response?.data || "Failed to update user";
      }
    },

    async deleteUser(id) {
      try {
        await axios.delete(`http://localhost:5000/users/${id}`);
        await this.fetchUsers();
      } catch (error) {
        this.error = error.response?.data || "Failed to delete user";
      }
    },

    async connection(user) {
      try {
        const res = await axios.post(`http://localhost:5000/users/login`, user);

        // ✅ Store token in localStorage
        const token = res.data.token;
        localStorage.setItem("token", token);

        // ✅ Optionally set it in the store too
        this.token = token;
        this.error = null;

        // ✅ Set default Authorization header for all future axios calls
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      } catch (error) {
        this.error = error.response?.data || "Failed to login user";
      }
    },
  },
});
