<!-- views/DashboardView.vue -->
<template>
  <div>
    <custom-title><span>Dashboard</span></custom-title>

    <!-- Summary Cards -->
    <v-row>
      <v-col cols="12" md="3">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="primary"
          theme="dark"
        >
          <v-icon size="48">mdi-account-multiple</v-icon>
          <v-card-title>
            Total Students
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">1,250</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="teal"
          theme="dark"
        >
          <v-icon size="48">mdi-account-tie-outline</v-icon>
          <v-card-title>
            Total Instructors
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">1,250</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="secondary"
          theme="dark"
        >
          <v-icon size="48">mdi-book-open-page-variant</v-icon>
          <v-card-title>
            Total Courses
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">85</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          class="d-flex flex-column align-center pa-4"
          color="error"
          theme="dark"
        >
          <v-icon size="48">mdi-clock-alert</v-icon>
          <v-card-title>
            Pending Approvals
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">12</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Recent Enrollments Table -->
    <v-row class="mt-8">
      <v-col cols="12">
        <v-card>
          <v-card-title class="bg-primary">
            Recent Enrollments
          </v-card-title>
          <v-data-table
            :headers="recentEnrollmentsHeaders"
            :items="recentEnrollments"
            items-per-page="5"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from "vue";

const recentEnrollmentsHeaders = [
  { title: "Enrollment ID", key: "id" },
  { title: "Date", key: "date" },
  { title: "Student Name", key: "student" },
  { title: "Course", key: "course" },
];

const recentEnrollments = ref([
  { id: "E001", date: "2025-08-05", student: "Alice Johnson", course: "CS-101: Intro to Programming" },
  { id: "E002", date: "2025-08-05", student: "Michael Smith", course: "BUS-201: Microeconomics" },
  { id: "E003", date: "2025-08-05", student: "Emma Davis", course: "ENG-305: Creative Writing" },
  { id: "E004", date: "2025-08-04", student: "James Lee", course: "MATH-210: Linear Algebra" },
  { id: "E005", date: "2025-08-04", student: "Sophia Wilson", course: "BIO-110: General Biology" },
]);
</script>

<style scoped>
/* Vuetify styling handles most design, but you can add custom tweaks here */
</style>
