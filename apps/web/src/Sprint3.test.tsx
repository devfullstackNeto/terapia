import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Agenda3, AIStatusCard } from './Sprint3'

afterEach(() => { cleanup(); vi.unstubAllGlobals() })

describe('Sprint 3 immersive UX', () => {
  it('AI-UX-001 mostra provider, modelo, RAG e safety', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ provider: 'ollama', label: 'IA local — Ollama / Mistral', model: 'mistral', available: true, mode: 'local', fallback: 'mock', rag_active: true, safety_active: true, knowledge_base: { published_versions: 5 } }) }))
    render(<AIStatusCard token="demo" />)
    expect(await screen.findByText('IA local — Ollama / Mistral')).toBeInTheDocument()
    expect(screen.getByText(/RAG ativo.*safety ativo/i)).toBeInTheDocument()
  })

  it('APPT-UX-001 alterna calendário entre mês e semana', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => [] }))
    render(<Agenda3 token="demo" />)
    const week = screen.getByRole('button', { name: 'Semana' })
    fireEvent.click(week)
    expect(week).toHaveClass('active')
    expect(screen.getByText('Hoje')).toBeInTheDocument()
  })
})
