<template>

  <custom-title class="mb-6">Student Transcript</custom-title>

  <v-card class="pa-6 mb-6 elevation-2">
    <v-row no-gutters class="align-center">
      <v-col cols="12" md="6">
        <div class="info-item">
          <span class="info-label">STUDENT NAME</span>
          <span class="info-value">{{ studentName }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">CLASS</span>
          <span class="info-value">{{ className }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">DATE</span>
          <span class="info-value">{{ formattedDate }}</span>
        </div>
      </v-col>

      <v-spacer class="d-none d-md-block"></v-spacer>

      <v-col cols="12" md="4" class="text-md-right mt-4 mt-md-0">
        <div class="score-summary-card">
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="score-label">TOTAL SCORE</span>
            <span class="score-value">{{ totalScore }}</span>
          </div>
          <div class="d-flex justify-space-between align-center mb-2">
            <span class="score-label">AVERAGE SCORE</span>
            <span class="score-value">{{ averageScore }}</span>
          </div>
          <v-divider class="my-2"></v-divider>
          <div class="d-flex justify-space-between align-center">
            <span class="gpa-label">GPA</span>
            <span class="gpa-value">{{ gpa }}</span>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-card>

  <v-row class="mb-6">
    <v-col cols="12">
      <v-menu v-model="menu" :close-on-content-click="false" location="start">
        <template #activator="{ props }">
          <v-btn color="primary" v-bind="props" class="text-none">
            <v-icon start>mdi-calendar-range</v-icon>
            Select Transcript Date
          </v-btn>
        </template>
        <v-date-picker v-model="selectedDate" @update:model-value="onDateChange"></v-date-picker>
      </v-menu>
    </v-col>
  </v-row>

  <v-card class="elevation-2">
    <v-data-table :headers="transcriptHeaders" :items="studentTranscript.subjects || []" :items-per-page="10"
      class="transcript-table">
      <template #item.score="{ item }">
        <span class="font-weight-medium">{{ item.score }}</span>
      </template>
      <template #item.grade="{ item }">
        <v-chip :color="getGradeColor(item.grade)" class="font-weight-bold">
          {{ item.grade }}
        </v-chip>
      </template>
      <template #item.remarks="{ item }">
        <span class="text-grey-darken-1">{{ item.remarks || '—' }}</span>
      </template>
    </v-data-table>
  </v-card>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useReportStore } from '../stores/reportStore'

const menu = ref(false)
const selectedDate = ref(new Date())
const reportStore = useReportStore()

// Computed properties (unmodified from original)
const studentTranscript = computed(() => reportStore.studentTranscript)
const studentName = computed(() => studentTranscript.value.studentName || 'N/A')
const className = computed(() => studentTranscript.value.className || 'N/A')
const formattedDate = computed(() => {
  if (!studentTranscript.value.date) return 'N/A'
  const dateObj = new Date(studentTranscript.value.date)
  return new Intl.DateTimeFormat('en-US', { day: '2-digit', month: '2-digit', year: '2-digit' }).format(dateObj)
})
const totalScore = computed(() => {
  if (!studentTranscript.value.subjects) return 0
  return studentTranscript.value.subjects.reduce((sum, subj) => sum + subj.score, 0)
})
const averageScore = computed(() => {
  if (!studentTranscript.value.subjects || studentTranscript.value.subjects.length === 0) return 0
  return (totalScore.value / studentTranscript.value.subjects.length).toFixed(2)
})
const gpa = computed(() => studentTranscript.value.gpa || 'N/A')
const transcriptHeaders = [
  { title: 'SUBJECT CODE', key: 'subjectCode' },
  { title: 'SUBJECT NAME', key: 'subjectName' },
  { title: 'SCORE', key: 'score' },
  { title: 'GRADE', key: 'grade' },
  { title: 'REMARKS', key: 'remarks' }
]

// Methods (unmodified from original)
function onDateChange(newDate) {
  menu.value = false
  if (newDate) {
    const dateString = newDate.toISOString().split('T')[0]
    reportStore.fetchStudentTranscript(dateString)
  }
}

function getGradeColor(grade) {
  switch (grade) {
    case 'A':
      return 'green-lighten-1'
    case 'B':
      return 'blue-lighten-1'
    case 'C':
      return 'amber-lighten-1'
    case 'D':
      return 'orange-lighten-1'
    case 'F':
      return 'red-lighten-1'
    default:
      return 'grey-lighten-1'
  }
}

// Load data on mount (unmodified from original)
onMounted(() => {
  const today = new Date().toISOString().split('T')[0]
  reportStore.fetchStudentTranscript(today)
})
</script>

<style scoped>
/* Styles for the student info section */
.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.info-label {
  font-weight: 600;
  color: #666;
  width: 140px;
  /* Fixed width for labels for alignment */
  flex-shrink: 0;
}

.info-value {
  font-weight: 400;
  color: #333;
}

/* Styles for the summary score card */
.score-summary-card {
  background-color: #f5f5f5;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.score-label {
  font-weight: 500;
  color: #555;
  font-size: 0.95rem;
}

.score-value {
  font-weight: 600;
  color: #333;
  font-size: 1.1rem;
}

.gpa-label {
  font-weight: 700;
  color: #1a237e;
  /* A standout color for GPA */
  font-size: 1.2rem;
}

.gpa-value {
  font-weight: 800;
  color: #1a237e;
  font-size: 2.2rem;
  /* Larger font size to highlight GPA */
}

/* Custom styling for the data table */
.transcript-table {
  border-radius: 8px;
}

.transcript-table :deep(th) {
  background-color: #e0e0e0 !important;
  color: #424242 !important;
  font-weight: 700 !important;
  text-transform: uppercase;
}

.transcript-table :deep(td) {
  padding: 16px !important;
}

.v-chip {
  min-width: 48px;
  /* Consistent width for grade chips */
  justify-content: center;
}
</style>