import { useState, useRef, useEffect } from 'react'

const WS_URL = 'ws://localhost:8000/ws'

const SCRIPTED_EVENTS = [
  { id: 'EVT-001', crop: 'Sugarcane', place: 'Sitapur', issue: 'Pyrilla (Leaf Hopper)' },
  { id: 'EVT-002', crop: 'Wheat', place: 'Hardoi', issue: 'Irrigation Failure' },
]

const AGENT_META = {
  'Field Monitor': { code: 'Monitor', color: '#3B82F6' },
  'Agronomist': { code: 'Agronomist', color: '#10B981' },
  'Resource Agent': { code: 'Resource', color: '#F59E0B' },
  'Scheme Agent': { code: 'Scheme', color: '#8B5CF6' },
  'Farmer Advisory': { code: 'Advisory', color: '#111827' },
}

export default function App() {
  const [timeline, setTimeline] = useState([])
  const [state, setState] = useState(null)
  const [connected, setConnected] = useState(false)
  const [running, setRunning] = useState(false)
  const [liveDescription, setLiveDescription] = useState('')
  const [liveCrop, setLiveCrop] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [classifying, setClassifying] = useState(false)
  
  // Live Session Analytics State
  const [casesProcessed, setCasesProcessed] = useState(0)
  const [executionTime, setExecutionTime] = useState('0.0s')
  
  const wsRef = useRef(null)
  const timerRef = useRef(null)
  const overrideRef = useRef(null) // Reference for the smooth scroll

  // Smooth scroll function for the "Report incident" button
  function scrollToInject() {
    overrideRef.current?.scrollIntoView({ behavior: 'smooth' })
    setTimeout(() => document.getElementById('anomaly-input')?.focus(), 400)
  }

  function runPayload(payload) {
    setTimeline([])
    setState(null)
    setRunning(true)
    
    timerRef.current = performance.now()

    const ws = new WebSocket(WS_URL)
    wsRef.current = ws

    ws.onopen = () => {
      setConnected(true)
      ws.send(JSON.stringify(payload))
    }

    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data)
      if (data.type === 'start') setState({ current_event: data.event })
      if (data.type === 'agent_update') {
        setTimeline((prev) => [...prev, { agent: data.agent, message: data.message, at: new Date() }])
        setState((prev) => ({ ...prev, ...data.state }))
      }
      if (data.type === 'complete') {
        setRunning(false)
        
        if (timerRef.current) {
          const timeTaken = ((performance.now() - timerRef.current) / 1000).toFixed(1)
          setExecutionTime(`${timeTaken}s`)
        }
        setCasesProcessed(prev => prev + 1)
        
        ws.close()
      }
    }

    ws.onclose = () => setConnected(false)
    ws.onerror = () => setRunning(false)
  }

  function runScripted(eventId) {
    runPayload({ event_id: eventId })
  }

  function runLiveInjection() {
    if (!liveDescription.trim()) return
    runPayload({ mode: 'custom', description: liveDescription, crop_type: liveCrop })
  }

  async function classifyAndInject() {
    if (!imageFile) return
    setClassifying(true)
    const formData = new FormData()
    formData.append('file', imageFile)

    try {
      const res = await fetch('http://localhost:8000/classify-image', { method: 'POST', body: formData })
      const result = await res.json()
      const description = liveDescription.trim() || "Analyze this uploaded field image."
      runPayload({ mode: 'custom', description, crop_type: liveCrop, base64_image: result.base64_image })
    } catch (err) {
      console.error('Image upload failed', err)
    } finally {
      setClassifying(false)
    }
  }

  return (
    <div className="flex h-screen bg-surface font-sans text-ink overflow-hidden">
      {/* --- SIDEBAR --- */}
      <aside className="w-[260px] bg-surface-panel border-r border-gray-200 flex flex-col flex-shrink-0">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 bg-brand rounded-lg flex items-center justify-center text-white font-bold text-lg">⌘</div>
          <div>
            <h1 className="font-bold text-sm tracking-wide">CRISIS ROOM</h1>
            <p className="text-[10px] text-ink-muted uppercase tracking-wider">Farm Operations</p>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-1 mt-2">
          <div className="px-3 py-2 text-xs font-semibold text-ink-dim bg-gray-100 rounded-md flex items-center justify-between mb-4">
            <span className="flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-green-500"></div>LIVE WORKSPACE</span>
            <span>v</span>
          </div>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-sm font-medium text-brand bg-brand-light rounded-md border border-brand/20">
            Overview
          </a>
          {/* Unnecessary dead links have been completely removed */}
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="bg-gray-50 p-3 rounded-lg flex items-center gap-3 mb-4">
            <div className={`w-8 h-8 rounded-md flex items-center justify-center ${connected ? 'bg-green-100 text-green-600' : 'bg-gray-200 text-gray-500'}`}>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"></path></svg>
            </div>
            <div>
              <p className="text-xs font-semibold">{connected ? 'WebSocket connected' : 'System Standby'}</p>
              <p className="text-[10px] text-ink-muted">All agents synced · Live</p>
            </div>
          </div>
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 bg-green-800 text-white rounded-md flex items-center justify-center font-bold text-xs">AH</div>
            <div>
              <p className="text-sm font-semibold">Abdul Hannan</p>
              <p className="text-[11px] text-ink-muted">Team Leader</p>
            </div>
          </div>
        </div>
      </aside>

      {/* --- MAIN CONTENT --- */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* TOPBAR */}
        <header className="h-14 bg-surface-panel border-b border-gray-200 flex items-center justify-between px-8 flex-shrink-0">
          <div className="text-sm text-ink-dim"><span className="text-ink-muted">Workspace →</span> Overview</div>
          <div className="flex items-center gap-4">
            <input type="text" placeholder="Search incidents..." className="text-sm px-4 py-1.5 border border-gray-200 rounded-md w-64 focus:outline-none focus:ring-1 focus:ring-brand" />
          </div>
        </header>

        {/* DASHBOARD SCROLL AREA */}
        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto space-y-6">
            
            {/* HERO BANNER */}
            <div className="bg-gray-900 rounded-2xl p-8 relative overflow-hidden shadow-sm" style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1586771107445-d3ca888129ff?q=80&w=2000&auto=format&fit=crop")', backgroundSize: 'cover', backgroundPosition: 'center' }}>
              <div className="absolute inset-0 bg-black/50"></div>
              <div className="relative z-10">
                <span className="text-brand text-xs font-bold tracking-widest uppercase mb-2 block flex items-center gap-2">
                  <div className="w-1.5 h-1.5 bg-brand rounded-full"></div> OPERATIONS CONTROL CENTER
                </span>
                <h2 className="text-3xl font-bold text-white mb-2">Good morning, Abdul.</h2>
                <p className="text-gray-300 text-sm mb-6">Here's what your farm intelligence network is seeing right now.</p>
                <div className="flex gap-3">
                  {/* The Report Incident button is now wired up to scroll down */}
                  <button onClick={scrollToInject} className="bg-brand hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
                    ⚠ Report incident
                  </button>
                  {/* The dead Filter button has been removed */}
                </div>
              </div>
            </div>

            {/* LIVE DYNAMIC KPI GRID */}
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'Active Pipeline', val: running ? '01' : '00', sub: running ? 'Processing stream...' : 'Standby', subColor: running ? 'text-amber-500' : 'text-gray-500', icon: 'bg-red-100 text-red-500' },
                { label: 'Agent Latency', val: running ? '...' : executionTime, sub: 'Last chain execution', subColor: 'text-green-600', icon: 'bg-green-100 text-green-600' },
                { label: 'Events Processed', val: casesProcessed < 10 ? `0${casesProcessed}` : casesProcessed, sub: 'This session', subColor: 'text-blue-600', icon: 'bg-blue-100 text-blue-500' },
                { label: 'Nodes Engaged', val: timeline.length < 10 ? `0${timeline.length}` : timeline.length, sub: 'Active agents', subColor: 'text-yellow-600', icon: 'bg-yellow-100 text-yellow-600' }
              ].map((kpi, i) => (
                <div key={i} className="bg-surface-panel p-5 rounded-xl border border-gray-200 shadow-sm flex items-center gap-4 transition-all">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${kpi.icon}`}>❖</div>
                  <div>
                    <p className="text-xs text-ink-dim">{kpi.label}</p>
                    <p className="text-2xl font-bold">{kpi.val}</p>
                    <p className={`text-[10px] ${kpi.subColor}`}>{kpi.sub}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* LOWER SPLIT: FEED vs DETAILS */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* LEFT: INJECTION / FEED */}
              <div className="space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-gray-200">
                  <h3 className="font-bold text-sm">Live incident feed</h3>
                  {running && (
                    <span className="text-[10px] font-bold text-green-600 bg-green-100 px-2 py-0.5 rounded uppercase tracking-wider flex items-center gap-1">
                      <div className="w-1.5 h-1.5 bg-green-500 rounded-full pulse-dot"></div> Live
                    </span>
                  )}
                </div>

                {/* Injection Form */}
                <div ref={overrideRef} className="bg-surface-panel p-4 rounded-xl border border-gray-200 shadow-sm scroll-mt-6">
                  <h4 className="text-xs font-bold text-brand mb-2">⚠ MANUAL OVERRIDE</h4>
                  <textarea
                    id="anomaly-input"
                    value={liveDescription}
                    onChange={(e) => setLiveDescription(e.target.value)}
                    placeholder="Describe field anomaly..."
                    className="w-full bg-gray-50 border border-gray-200 rounded-lg p-2 text-sm focus:ring-1 focus:ring-brand focus:outline-none mb-2"
                    rows="2"
                  />
                  <input
                    type="file"
                    onChange={(e) => setImageFile(e.target.files[0])}
                    className="w-full text-xs text-ink-dim mb-3 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:bg-gray-100 file:text-brand cursor-pointer"
                  />
                  <div className="flex gap-2">
                    <button onClick={imageFile ? classifyAndInject : runLiveInjection} disabled={running || (!liveDescription && !imageFile)} className="flex-1 bg-ink hover:bg-gray-800 text-white py-1.5 rounded-lg text-xs font-bold disabled:opacity-50 transition-colors">
                      {classifying ? 'ANALYZING...' : 'RUN PIPELINE →'}
                    </button>
                  </div>
                </div>

                {/* Scripted Events List */}
                <div className="space-y-2">
                  {SCRIPTED_EVENTS.map((e) => (
                    <div key={e.id} onClick={() => !running && runScripted(e.id)} className={`p-3 rounded-xl border cursor-pointer transition-colors ${state?.current_event?.event_id === e.id ? 'bg-brand-light border-brand' : 'bg-surface-panel border-gray-200 hover:border-gray-300'}`}>
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-sm font-bold">{e.issue}</span>
                        <span className="text-[10px] text-ink-muted">{e.id}</span>
                      </div>
                      <div className="text-xs text-ink-dim">{e.crop} · {e.place}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* RIGHT: AGENT OUTPUT DETAILS */}
              <div className="lg:col-span-2 space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-gray-200">
                  <h3 className="font-bold text-sm">Selected incident</h3>
                  <span className="text-[10px] text-ink-muted"> {state?.current_event?.event_id || 'Waiting for signal...'}</span>
                </div>

                {state?.current_event ? (
                  <div className="bg-surface-panel rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col h-[500px]">
                    {/* Header Block */}
                    <div className="p-5 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                       <div>
                         <h4 className="font-bold text-lg">{state.current_event.crop_type} Anomaly</h4>
                         <p className="text-xs text-ink-dim">{state.current_event.location}</p>
                       </div>
                       {state.anomaly_severity && (
                         <div className="text-right">
                           <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded ${state.anomaly_severity.toLowerCase().includes('high') ? 'text-red-600 bg-red-100' : state.anomaly_severity.toLowerCase().includes('medium') ? 'text-amber-600 bg-amber-100' : 'text-green-600 bg-green-100'}`}>
                             {state.anomaly_severity} PRIORITY
                           </span>
                           {state.estimated_loss_percent && <p className="text-xs text-ink-dim mt-1">{state.estimated_loss_percent}% Loss Risk</p>}
                         </div>
                       )}
                    </div>
                    
                    {/* Agent Chain Timeline */}
                    <div className="flex-1 overflow-y-auto p-5 space-y-4">
                      {timeline.length === 0 && <p className="text-sm text-ink-muted italic">Processing environmental data...</p>}
                      {timeline.map((entry, i) => {
                        const meta = AGENT_META[entry.agent] || { code: entry.agent, color: '#9CA3AF' }
                        return (
                          <div key={i} className="flex gap-3">
                            <div className="w-1.5 rounded-full mt-1.5 mb-1 flex-shrink-0" style={{ backgroundColor: meta.color }}></div>
                            <div>
                              <span className="text-xs font-bold uppercase tracking-wide" style={{ color: meta.color }}>{meta.code}</span>
                              <p className="text-sm text-ink mt-0.5 leading-relaxed">{entry.message}</p>
                            </div>
                          </div>
                        )
                      })}
                      {running && <div className="flex gap-2 items-center text-xs text-brand font-medium"><div className="w-4 h-4 border-2 border-brand border-t-transparent rounded-full animate-spin"></div> Agents working...</div>}
                    </div>

                    {/* Final Farmer Advisory Box */}
                    {state.farmer_advisory && (
                      <div className="p-4 bg-green-50 border-t border-green-100">
                        <h5 className="text-xs font-bold text-green-800 uppercase tracking-wide mb-2">Outbound Advisory</h5>
                        <p className="text-sm text-green-900">{state.farmer_advisory}</p>
                        
                        {state.matched_schemes?.length > 0 && (
                          <div className="mt-3 flex flex-wrap gap-2">
                            {state.matched_schemes.map((s, idx) => (
                              <span key={idx} className="bg-white border border-green-200 text-green-700 text-[10px] px-2 py-1 rounded font-bold shadow-sm">{s.scheme}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="h-[500px] border border-dashed border-gray-300 rounded-xl flex items-center justify-center text-ink-muted text-sm bg-gray-50">
                    No active incident selected. Inject a live event to begin.
                  </div>
                )}
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  )
}