import { FormEvent, useEffect, useState } from 'react'

import { apiClient } from './api/client'
import { Section } from './components/Section'
import type { DocumentUploadResponse, HealthResponse, SecurityStatusResponse, TaskResponse } from './types'

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [security, setSecurity] = useState<SecurityStatusResponse | null>(null)
  const [tasks, setTasks] = useState<TaskResponse[]>([])
  const [uploaded, setUploaded] = useState<DocumentUploadResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [title, setTitle] = useState('Inspection report summary')
  const [prompt, setPrompt] = useState('Analyze findings and prepare output package')
  const [requiresReview, setRequiresReview] = useState(true)

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError(null)
      try {
        const [h, s, t] = await Promise.all([
          apiClient.getHealth(),
          apiClient.getSecurityStatus(),
          apiClient.listTasks()
        ])
        setHealth(h)
        setSecurity(s)
        setTasks(t)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }

    void load()
  }, [])

  const onUpload = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const input = event.currentTarget.elements.namedItem('document') as HTMLInputElement
    const file = input.files?.[0]
    if (!file) {
      return
    }
    setError(null)
    try {
      const response = await apiClient.uploadDocument(file)
      setUploaded(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    }
  }

  const onCreateTask = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    try {
      const created = await apiClient.createTask({
        title,
        prompt,
        requires_review: requiresReview
      })
      setTasks((prev) => [created, ...prev])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Task creation failed')
    }
  }

  return (
    <main className="container">
      <h1>SovereignAI Workbench Dashboard</h1>
      {loading && <p>Loading dashboard…</p>}
      {error && <p className="error">{error}</p>}

      <Section title="Health Status">
        {health ? <p>{health.service}: {health.status}</p> : <p>No health data yet.</p>}
      </Section>

      <Section title="Document Upload">
        <form onSubmit={onUpload}>
          <input name="document" type="file" accept=".txt,.md,.pdf,.png,.jpg,.jpeg" />
          <button type="submit">Upload</button>
        </form>
        {uploaded ? <p>Uploaded: {uploaded.filename} ({uploaded.size_bytes} bytes)</p> : <p>No document uploaded.</p>}
      </Section>

      <Section title="Task Creation">
        <form onSubmit={onCreateTask} className="form-grid">
          <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Task title" required />
          <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={3} required />
          <label>
            <input
              type="checkbox"
              checked={requiresReview}
              onChange={(e) => setRequiresReview(e.target.checked)}
            />
            Require review
          </label>
          <button type="submit">Create Task</button>
        </form>
      </Section>

      <Section title="Task Progress and Events">
        {tasks.length === 0 ? (
          <p>No tasks yet.</p>
        ) : (
          <ul>
            {tasks.map((task) => (
              <li key={task.task_id}>
                <strong>{task.title}</strong> — {task.status} ({task.events.length} events)
              </li>
            ))}
          </ul>
        )}
      </Section>

      <Section title="Generated Outputs">
        {tasks.length === 0 ? (
          <p>No generated outputs yet.</p>
        ) : (
          <ul>
            {tasks.flatMap((task) =>
              task.output_files.map((file) => (
                <li key={`${task.task_id}-${file}`}>{file}</li>
              ))
            )}
          </ul>
        )}
      </Section>

      <Section title="Security / Offline Status">
        {security ? (
          <ul>
            <li>Offline mode configured: {String(security.offline_mode)}</li>
            <li>Model endpoint: {security.model_endpoint}</li>
            <li>Endpoint local-only: {String(security.model_endpoint_local)}</li>
            <li>Endpoint reachable: {String(security.model_endpoint_reachable)}</li>
          </ul>
        ) : (
          <p>No security status yet.</p>
        )}
      </Section>
    </main>
  )
}

export default App
