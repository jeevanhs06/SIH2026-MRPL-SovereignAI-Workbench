export type HealthResponse = {
  status: string
  service: string
}

export type DocumentUploadResponse = {
  document_id: string
  filename: string
  extension: string
  size_bytes: number
  checksum_sha256: string
  stored_path: string
}

export type TaskStatus =
  | 'created'
  | 'queued'
  | 'running'
  | 'waiting_for_review'
  | 'completed'
  | 'failed'
  | 'rejected'

export type TaskEvent = {
  timestamp: string
  event: string
  details: Record<string, string>
}

export type TaskResponse = {
  task_id: string
  title: string
  prompt: string
  status: TaskStatus
  document_ids: string[]
  requires_review: boolean
  output_files: string[]
  created_at: string
  updated_at: string
  events: TaskEvent[]
}

export type SecurityStatusResponse = {
  offline_mode: boolean
  model_endpoint: string
  model_endpoint_local: boolean
  model_endpoint_reachable: boolean
  note: string
}
