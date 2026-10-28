import { useEffect, useRef, useState } from 'react'
import { Send } from 'lucide-react'
import { api } from '../services/api'
import { PageHead } from '../components/ui'

const SUGGESTIONS = [
  'Which phone has the best camera?',
  'What are common complaints about Pulse Lite 4?',
  'Recommend headphones with good sound under $200',
  'Compare Nova X1 Pro and Aero Max Ultra',
]

export default function Assistant() {
  const [messages, setMessages] = useState([{ role: 'bot', text: 'Ask me anything about the products and their reviews.' }])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const logRef = useRef(null)

  useEffect(() => { if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight }, [messages])

  async function send(text) {
    const msg = (text ?? input).trim()
    if (!msg || busy) return
    setInput(''); setMessages((m) => [...m, { role: 'user', text: msg }]); setBusy(true)
    try {
      const res = await api.chat(msg, messages.map((m) => ({ role: m.role, text: m.text })))
      setMessages((m) => [...m, { role: 'bot', text: res.reply }])
    } catch (e) { setMessages((m) => [...m, { role: 'bot', text: `Error: ${e.message}` }]) }
    finally { setBusy(false) }
  }

  return (
    <div style={{ maxWidth: 760, margin: '0 auto' }}>
      <PageHead title="AI product assistant">
        A local retrieval assistant that answers from the analyzed product and review data (no external LLM).
      </PageHead>
      <div className="card">
        <div className="chat-log" ref={logRef} style={{ maxHeight: '50vh' }}>
          {messages.map((m, i) => <div key={i} className={`msg ${m.role === 'user' ? 'user' : 'bot'}`}>{m.text}</div>)}
        </div>
        <div className="tag-list" style={{ margin: '12px 0' }}>
          {SUGGESTIONS.map((s) => <button key={s} className="chip" style={{ cursor: 'pointer', border: 0 }} onClick={() => send(s)}>{s}</button>)}
        </div>
        <form className="row" style={{ flexWrap: 'nowrap' }} onSubmit={(e) => { e.preventDefault(); send() }}>
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type your question…" />
          <button className="btn" disabled={busy}><Send size={15} /> Send</button>
        </form>
      </div>
    </div>
  )
}
