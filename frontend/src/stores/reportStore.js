import { defineStore } from 'pinia'
import http from '../api/api' // your axios instance

export const useReportStore = defineStore('report', {
  state: () => ({
    studentTranscript: [],
    expiredItems: []
  }),
  actions: {
    async fetchStudentTranscript() {
      const res = await http.get('/reports/daily-sales')
      console.log(res);
      
      this.studentTranscript = res.data
    },
    async fetchExpiredItems() {
      const res = await http.get('/reports/expired-items')
      this.expiredItems = res.data
    }
  }
})
