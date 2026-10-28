import { useRef, useState, useEffect } from 'react'
import { MessageCircle, X, Send } from 'lucide-react'
import { api } from '../services/api'

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hi! Ask me about products, reviews or recommendations.' },
  ])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const logRef = useRef(null)

  useEffect(() => { if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight }, [messages, open])

  async function send(e) {
    e.preventDefault()
    const text = input.trim()
    if (!text || busy) return
    setInput('')
    setMessages((m) => [...m, { role: 'user', text }])
    setBusy(true)
    try {
      const res = await api.chat(text, messages.map((m) => ({ role: m.role, text: m.text })))
      setMessages((m) => [...m, { role: 'bot', text: res.reply }])
    } catch (err) {
      setMessages((m) => [...m, { role: 'bot', text: `Error: ${err.message}` }])
    } finally { setBusy(false) }
  }

  return (
    <>
      <button className="btn" onClick={() => setOpen((o) => !o)}
        style={{ position: 'fixed', right: 20, bottom: 20, borderRadius: 999, zIndex: 60, boxShadow: 'var(--shadow)' }}>
        {open ? <X size={16} /> : <MessageCircle size={16} />} Assistant
      </button>
      {open && (
        <div className="card" style={{ position: 'fixed', right: 20, bottom: 74, width: 340, maxWidth: '92vw', zIndex: 60, padding: 14 }}>
          <strong style={{ color: 'var(--forest)' }}>Product Assistant</strong>
          <div className="chat-log" ref={logRef} style={{ margin: '10px 0' }}>
            {messages.map((m, i) => <div key={i} className={`msg ${m.role === 'user' ? 'user' : 'bot'}`}>{m.text}</div>)}
          </div>
          <form onSubmit={send} className="row" style={{ flexWrap: 'nowrap' }}>
            <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask a question…" />
            <button className="btn sm" disabled={busy}><Send size={14} /></button>
          </form>
        </div>
      )}
    </>
  )
}
