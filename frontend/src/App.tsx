import { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

interface ActionItem {
  task: string
  owner: string
  due: string
  priority: string
}

interface MeetingResult {
  meeting_id: string
  summary: string
  action_items: ActionItem[]
  decisions: string[]
  open_questions: string[]
}

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [emails, setEmails] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MeetingResult | null>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError('')
    const form = new FormData()
    form.append('audio', file)
    form.append('attendee_emails', emails)
    try {
      const { data } = await axios.post(`${API_BASE}/api/meetings/process`, form)
      setResult(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Processing failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', maxWidth: 760, margin: '40px auto', padding: '0 20px' }}>
      <h1>🎤 SmartMeet AI</h1>
      <p style={{ color: '#666' }}>Upload a meeting recording. Get structured summary, action items, and decisions instantly.</p>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <input type="file" accept="audio/*" onChange={e => setFile(e.target.files?.[0] || null)} required />
        <input type="text" placeholder="Attendee emails (comma-separated, optional)" value={emails} onChange={e => setEmails(e.target.value)} style={{ padding: 8, border: '1px solid #ccc', borderRadius: 4 }} />
        <button type="submit" disabled={loading || !file} style={{ padding: '10px 20px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
          {loading ? 'Processing...' : 'Process Meeting'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div style={{ marginTop: 32 }}>
          <h2>Summary</h2>
          <p>{result.summary}</p>
          <h2>Action Items</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead><tr style={{ background: '#f3f4f6' }}><th style={{ padding: 8, textAlign: 'left' }}>Task</th><th>Owner</th><th>Due</th><th>Priority</th></tr></thead>
            <tbody>{result.action_items.map((a, i) => (
              <tr key={i} style={{ borderBottom: '1px solid #e5e7eb' }}>
                <td style={{ padding: 8 }}>{a.task}</td><td>{a.owner}</td><td>{a.due}</td><td>{a.priority}</td>
              </tr>
            ))}</tbody>
          </table>
          <h2>Decisions</h2>
          <ul>{result.decisions.map((d, i) => <li key={i}>{d}</li>)}</ul>
          {result.open_questions.length > 0 && (<><h2>Open Questions</h2><ul>{result.open_questions.map((q, i) => <li key={i}>{q}</li>)}</ul></>)}
        </div>
      )}
    </div>
  )
}
