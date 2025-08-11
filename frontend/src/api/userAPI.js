import http from './api'

export function fetchAllUsers() {
  return http.get(`/users/`)
}
