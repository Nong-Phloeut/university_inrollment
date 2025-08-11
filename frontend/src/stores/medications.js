import { defineStore } from 'pinia'
import * as api from '../api/medicationsAPI'

export const useMedicationStore = defineStore('medication', {
  state: () => ({
    medications: []
  }),

  actions: {
    async fetchMedications() {
      const res = await api.fetchAllMedications()
      this.medications = res.data
    },

    async createMedication(data) {
      await api.createMedication(data)
      await this.fetchMedications()
    },

    async updateMedication(id, data) {
      await api.updateMedication(id, data)
      await this.fetchMedications()
    },

    async deleteMedication(id) {
      await api.deleteMedication(id)
      await this.fetchMedications()
    }
  }
})
