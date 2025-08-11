<template>

  <custom-title class="mb-6">Student Course Enrollment
    <template #right>
      <v-btn color="primary" prepend-icon="mdi-plus-circle" @click="openDialog">
        Add New Student
      </v-btn>
    </template>
  </custom-title>

  <v-card class="pa-4 mb-6 elevation-2">
    <v-row align="center">
      <v-col cols="12" md="4">
        <v-text-field v-model="search" label="Search by Name or ID" prepend-inner-icon="mdi-magnify" variant="outlined"
          hide-details clearable></v-text-field>
      </v-col>
    </v-row>
  </v-card>

  <v-card class="elevation-2">
    <v-data-table :headers="enrollmentHeaders" :items="filteredStudents" :search="search" :items-per-page="10"
      class="enrollment-table">
      <template #item.enrollmentDate="{ item }">
        <span class="text-medium-emphasis">{{ formatDate(item.enrollmentDate) }}</span>
      </template>
      <template #item.status="{ item }">
        <v-chip :color="getStatusColor(item.status)" class="font-weight-bold" size="small">
          {{ item.status }}
        </v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-btn icon size="small" color="primary" class="me-2">
          <v-icon>mdi-pencil</v-icon>
          <v-tooltip activator="parent" location="top">Edit</v-tooltip>
        </v-btn>
        <v-btn icon size="small" color="red">
          <v-icon>mdi-delete</v-icon>
          <v-tooltip activator="parent" location="top">Delete</v-tooltip>
        </v-btn>
      </template>
    </v-data-table>
  </v-card>
  <!-- Add Student Dialog -->
  <v-dialog v-model="showDialog" max-width="600px">
    <v-card>
      <v-card-title class="bg-primary">
        Add New Student Enrollment
      </v-card-title>

      <v-card-text>
        <v-form ref="addStudentForm" v-model="formValid">
          <v-text-field v-model="newStudent.name" label="Student Name" variant="outlined"
            :rules="[v => !!v || 'Name is required']" required></v-text-field>

          <v-text-field v-model="newStudent.studentId" label="Student ID" variant="outlined"
            :rules="[v => !!v || 'ID is required']" required></v-text-field>

          <v-text-field v-model="newStudent.program" label="Enrolled Program" variant="outlined"
            :rules="[v => !!v || 'Program is required']" required></v-text-field>

          <v-text-field v-model="newStudent.enrollmentDate" label="Enrollment Date" type="date" variant="outlined"
            :rules="[v => !!v || 'Date is required']" required></v-text-field>

          <v-select v-model="newStudent.status" label="Status" :items="['Active', 'Inactive', 'Suspended']"
            variant="outlined" :rules="[v => !!v || 'Status is required']" required></v-select>
        </v-form>
      </v-card-text>

      <v-card-actions class="justify-end">
        <v-btn text @click="closeDialog">Cancel</v-btn>
        <v-btn color="primary" @click="saveStudent">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from "vue";

const search = ref('');
const showDialog = ref(false);
const formValid = ref(false);
const addStudentForm = ref(null);

const newStudent = ref({
  name: "",
  studentId: "",
  program: "",
  enrollmentDate: "",
  status: "Active"
});


const enrollmentHeaders = [
  { title: "Student Name", key: "name" },
  { title: "Student ID", key: "studentId" },
  { title: "Enrolled Program", key: "program" },
  { title: "Enrollment Date", key: "enrollmentDate" },
  { title: "Status", key: "status" },
  { title: "Actions", key: "actions", sortable: false, align: 'end' },
];

const enrolledStudents = ref([
  { name: "Alice Johnson", studentId: "S-101", program: "Computer Science", enrollmentDate: "2024-09-01", status: "Active" },
  { name: "Bob Williams", studentId: "S-102", program: "Business Administration", enrollmentDate: "2024-08-15", status: "Active" },
  { name: "Charlie Brown", studentId: "S-103", program: "Mechanical Engineering", enrollmentDate: "2024-09-01", status: "Inactive" },
  { name: "Diana Prince", studentId: "S-104", program: "Fine Arts", enrollmentDate: "2024-09-10", status: "Active" },
  { name: "Eve Adams", studentId: "S-105", program: "Psychology", enrollmentDate: "2024-08-20", status: "Suspended" },
  { name: "Frank Miller", studentId: "S-106", program: "Computer Science", enrollmentDate: "2024-09-05", status: "Active" },
  { name: "Grace Lee", studentId: "S-107", program: "Business Administration", enrollmentDate: "2024-08-25", status: "Active" },
  { name: "Heidi Turner", studentId: "S-108", program: "Mechanical Engineering", enrollmentDate: "2024-09-12", status: "Active" },
]);

const filteredStudents = computed(() => {
  if (!search.value) {
    return enrolledStudents.value;
  }
  const searchText = search.value.toLowerCase();
  return enrolledStudents.value.filter(student =>
    student.name.toLowerCase().includes(searchText) ||
    student.studentId.toLowerCase().includes(searchText)
  );
});

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

function getStatusColor(status) {
  switch (status) {
    case 'Active':
      return 'green-lighten-1';
    case 'Inactive':
      return 'grey-lighten-1';
    case 'Suspended':
      return 'red-lighten-1';
    default:
      return 'grey-lighten-1';
  }
}

function openDialog() {
  showDialog.value = true;
}
function closeDialog() {
  showDialog.value = false;
  resetForm();
}
function resetForm() {
  newStudent.value = {
    name: "",
    studentId: "",
    program: "",
    enrollmentDate: "",
    status: "Active"
  };
}
function saveStudent() {
  if (addStudentForm.value.validate()) {
    enrolledStudents.value.push({ ...newStudent.value });
    closeDialog();
  }
}

</script>

<style scoped>
.custom-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
}

.enrollment-table :deep(th) {
  background-color: #e0e0e0 !important;
  color: #424242 !important;
  font-weight: 700 !important;
  text-transform: uppercase;
}


.v-chip {
  min-width: 80px;
  /* Give status chips a consistent width */
  justify-content: center;
}
</style>