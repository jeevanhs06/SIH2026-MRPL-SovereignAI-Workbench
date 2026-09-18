import { render } from '@testing-library/react'
import { vi } from 'vitest'

import App from './App'

vi.stubGlobal('fetch', vi.fn(async (url: string) => {
  if (url.endsWith('/health')) {
    return new Response(JSON.stringify({ status: 'ok', service: 'backend' }), { status: 200 })
  }
  if (url.endsWith('/security/network-status')) {
    return new Response(
      JSON.stringify({
        offline_mode: true,
        model_endpoint: 'http://127.0.0.1:11434',
        model_endpoint_local: true,
        model_endpoint_reachable: false,
        note: 'placeholder'
      }),
      { status: 200 }
    )
  }
  if (url.endsWith('/tasks')) {
    return new Response(JSON.stringify([]), { status: 200 })
  }
  return new Response('{}', { status: 404 })
}) as typeof fetch)

describe('App', () => {
  it('renders dashboard heading', async () => {
    const { findByText } = render(<App />)
    expect(await findByText(/SovereignAI Workbench Dashboard/i)).toBeInTheDocument()
  })
})
