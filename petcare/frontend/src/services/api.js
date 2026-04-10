import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 10000,
})

// Pets
export const petsAPI = {
  list: (ativo = true) => api.get(`/api/v1/pets/?ativo=${ativo}`),
  get: (id) => api.get(`/api/v1/pets/${id}`),
  create: (data) => api.post('/api/v1/pets/', data),
  update: (id, data) => api.put(`/api/v1/pets/${id}`, data),
  delete: (id) => api.delete(`/api/v1/pets/${id}`),
  dashboard: (id) => api.get(`/api/v1/pets/${id}/dashboard`),
}

// Raças
export const racasAPI = {
  list: (especie) => api.get('/api/v1/racas/', { params: especie ? { especie } : {} }),
  get: (id) => api.get(`/api/v1/racas/${id}`),
  create: (data) => api.post('/api/v1/racas/', data),
}

// Vacinas
export const vacinasAPI = {
  listByPet: (petId) => api.get(`/api/v1/vacinas/pet/${petId}`),
  pendentes: () => api.get('/api/v1/vacinas/pendentes'),
  create: (data) => api.post('/api/v1/vacinas/', data),
  update: (id, data) => api.put(`/api/v1/vacinas/${id}`, data),
  delete: (id) => api.delete(`/api/v1/vacinas/${id}`),
}

// Atividades
export const atividadesAPI = {
  listByPet: (petId) => api.get(`/api/v1/atividades/pet/${petId}`),
  sugestoes: (petId) => api.get(`/api/v1/atividades/sugestoes/${petId}`),
  create: (data) => api.post('/api/v1/atividades/', data),
  delete: (id) => api.delete(`/api/v1/atividades/${id}`),
}

// Passeios
export const passeiosAPI = {
  listByPet: (petId) => api.get(`/api/v1/passeios/pet/${petId}`),
  sugestoes: (petId) => api.get(`/api/v1/passeios/sugestoes/${petId}`),
  create: (data) => api.post('/api/v1/passeios/', data),
  delete: (id) => api.delete(`/api/v1/passeios/${id}`),
}

// Cuidados
export const cuidadosAPI = {
  listByRaca: (racaId, categoria) =>
    api.get(`/api/v1/cuidados/raca/${racaId}`, { params: categoria ? { categoria } : {} }),
  create: (data) => api.post('/api/v1/cuidados/', data),
  delete: (id) => api.delete(`/api/v1/cuidados/${id}`),
}

export default api
