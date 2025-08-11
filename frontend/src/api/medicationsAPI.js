import http from './api' // or './api' if that's your actual path

export function fetchAllMedications() {
  return http.get('/medications/')
}

export function fetchMedicationById(id) {
  return http.get(`/medications/${id}`)
}

export function createMedication(data) {
  return http.post('/medications', data)
}

export function updateMedication(id, data) {
  return http.put(`/medications/${id}`, data)
}

export function deleteMedication(id) {
  return http.delete(`/medications/${id}`)
}
