import type {
  DocumentUploadResponse,
  HealthResponse,
  SecurityStatusResponse,
  TaskResponse
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return (await response.json()) as T
}

export const apiClient = {
  getHealth: () => request<HealthResponse>('/health'),
  getSecurityStatus: () => request<SecurityStatusResponse>('/security/network-status'),
  listTasks: () => request<TaskResponse[]>('/tasks'),
  createTask: (payload: { title: string; prompt: string; requires_review: boolean }) =>
    request<TaskResponse>('/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }),
  uploadDocument: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return request<DocumentUploadResponse>('/documents/upload', {
      method: 'POST',
      body: formData
    })
  }
}
