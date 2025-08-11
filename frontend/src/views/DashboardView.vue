<!-- views/DashboardView.vue -->
<template>
  <div>
    <custom-title><span>Dashboard</span></custom-title>
    <!-- Summary Cards -->
    <v-row>
      <v-col cols="12" md="4">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="primary"
          theme="dark"
        >
          <v-icon size="48">mdi-cash-multiple</v-icon>
          <v-card-title class="text-h5 font-weight-bold"
            >Total Sales Today</v-card-title
          >
          <v-card-text class="text-h4 font-weight-bold">$1,250.00</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="secondary"
          theme="dark"
        >
          <v-icon size="48">mdi-pill</v-icon>
          <v-card-title class="text-h5 font-weight-bold"
            >Total Medications</v-card-title
          >
          <v-card-text class="text-h4 font-weight-bold">542</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="error"
          theme="dark"
        >
          <v-icon size="48">mdi-alert-circle</v-icon>
          <v-card-title class="text-h5 font-weight-bold"
            >Expired Items</v-card-title
          >
          <v-card-text class="text-h4 font-weight-bold">12</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Sales Table -->
    <v-row class="mt-8">
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h6 font-weight-bold"
            >Recent Sales</v-card-title
          >
          <v-data-table
            :headers="recentSalesHeaders"
            :items="recentSales"
            items-per-page="5"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from "vue";

const recentSalesHeaders = [
  { title: "Sale ID", key: "id" },
  { title: "Date", key: "date" },
  { title: "Total Amount", key: "amount" },
  { title: "Pharmacist", key: "pharmacist" },
];

const recentSales = ref([
  { id: "S001", date: "2025-08-05", amount: "$55.00", pharmacist: "John Doe" },
  {
    id: "S002",
    date: "2025-08-05",
    amount: "$12.50",
    pharmacist: "Jane Smith",
  },
  { id: "S003", date: "2025-08-05", amount: "$150.75", pharmacist: "John Doe" },
  {
    id: "S004",
    date: "2025-08-04",
    amount: "$20.00",
    pharmacist: "Peter Jones",
  },
  {
    id: "S005",
    date: "2025-08-04",
    amount: "$75.25",
    pharmacist: "Jane Smith",
  },
]);
</script>

<style scoped>
/* No scoped styles needed as Vuetify handles most of it */
</style>
