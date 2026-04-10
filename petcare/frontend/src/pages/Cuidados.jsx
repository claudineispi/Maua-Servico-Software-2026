import { useState, useEffect } from 'react'
import { racasAPI, cuidadosAPI } from '../services/api'
import { Heart, Plus, X, Trash2 } from 'lucide-react'

export default function Cuidados() {
  const [racas, setRacas] = useState([])
  const [racaId, setRacaId] = useState('')
  const [cuidados, setCuidados] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadingCuidados, setLoadingCuidados] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    categoria: 'alimentacao', titulo: '', descricao: '', frequencia: '', prioridade: 'media',
  })

  useEffect(() => {
    racasAPI.list().then(r => setRacas(r.data)).finally(() => setLoading(false))
  }, [])

  const loadCuidados = () => {
    if (!racaId) { setCuidados([]); return }
    setLoadingCuidados(true)
    cuidadosAPI.listByRaca(racaId).then(r => setCuidados(r.data)).finally(() => setLoadingCuidados(false))
  }

  useEffect(loadCuidados, [racaId])

  const save = async () => {
    if (!racaId) { setError('Selecione uma raca primeiro.'); return }
    if (!form.titulo || !form.descricao) { setError('Titulo e descricao sao obrigatorios.'); return }
    setError('')
    setSaving(true)
    try {
      await cuidadosAPI.create({ ...form, raca_id: parseInt(racaId) })
      setShowForm(false)
      setForm({ categoria: 'alimentacao', titulo: '', descricao: '', frequencia: '', prioridade: 'media' })
      loadCuidados()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar cuidado.')
    } finally {
      setSaving(false)
    }
  }

  const del = async (id) => {
    if (!confirm('Remover este cuidado?')) return
    try { await cuidadosAPI.delete(id); loadCuidados() } catch { alert('Erro ao remover.') }
  }

  if (loading) return <div className="spinner" />

  const prioColor = { alta: 'badge-orange', media: 'badge-blue', baixa: 'badge-gray' }
  const categorias = ['alimentacao', 'higiene', 'saude', 'comportamento', 'exercicio']

  return (
    <div>
      <div className="page-header">
        <h2>Guia de Cuidados</h2>
        <p>Cuidados especificos por raca: alimentacao, higiene, saude e mais</p>
      </div>

      <div style={{ display: 'flex', gap: 12, alignItems: 'flex-end', marginBottom: 28, flexWrap: 'wrap' }}>
        <div className="form-group" style={{ maxWidth: 360, marginBottom: 0 }}>
          <label className="form-label">Selecione a raca</label>
          <select className="form-select" value={racaId} onChange={e => setRacaId(e.target.value)}>
            <option value="">Escolha uma raca...</option>
            {racas.map(r => (
              <option key={r.id} value={r.id}>{r.nome} ({r.especie})</option>
            ))}
          </select>
        </div>
        {racaId && (
          <button className="btn btn-primary" onClick={() => { setShowForm(s => !s); setError('') }}>
            {showForm ? <X size={16} /> : <Plus size={16} />} {showForm ? 'Cancelar' : 'Novo Cuidado'}
          </button>
        )}
      </div>

      {showForm && racaId && (
        <div className="card" style={{ marginBottom: 24, background: 'var(--moss-pale)' }}>
          {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Categoria *</label>
              <select className="form-select" value={form.categoria} onChange={e => setForm(f => ({ ...f, categoria: e.target.value }))}>
                {categorias.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Prioridade</label>
              <select className="form-select" value={form.prioridade} onChange={e => setForm(f => ({ ...f, prioridade: e.target.value }))}>
                <option value="alta">Alta</option>
                <option value="media">Media</option>
                <option value="baixa">Baixa</option>
              </select>
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Titulo *</label>
            <input className="form-input" value={form.titulo} onChange={e => setForm(f => ({ ...f, titulo: e.target.value }))} placeholder="Ex: Escovacao do pelo" />
          </div>
          <div className="form-group">
            <label className="form-label">Descricao *</label>
            <textarea className="form-textarea" value={form.descricao} onChange={e => setForm(f => ({ ...f, descricao: e.target.value }))} placeholder="Descreva o cuidado em detalhes..." />
          </div>
          <div className="form-group" style={{ maxWidth: 300 }}>
            <label className="form-label">Frequencia</label>
            <input className="form-input" value={form.frequencia} onChange={e => setForm(f => ({ ...f, frequencia: e.target.value }))} placeholder="Ex: diario, semanal, mensal" />
          </div>
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? 'Salvando...' : '🩺 Salvar Cuidado'}
          </button>
        </div>
      )}

      {loadingCuidados && <div className="spinner" />}

      {!racaId && !loadingCuidados && (
        <div className="empty-state">
          <div className="emoji">🩺</div>
          <h3>Selecione uma raca acima</h3>
          <p>Os cuidados serao exibidos de acordo com a raca escolhida.</p>
        </div>
      )}

      {racaId && !loadingCuidados && cuidados.length === 0 && (
        <div className="empty-state">
          <div className="emoji">🩺</div>
          <h3>Nenhum cuidado cadastrado para esta raca</h3>
          <p>Clique em "Novo Cuidado" para adicionar.</p>
        </div>
      )}

      {cuidados.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {cuidados.map(c => (
            <div key={c.id} className="card" style={{ padding: '18px 22px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', marginBottom: 6 }}>
                    <strong style={{ color: 'var(--bark)', fontFamily: 'var(--font-display)' }}>{c.titulo}</strong>
                    <span className={`badge ${prioColor[c.prioridade] || 'badge-gray'}`}>{c.prioridade}</span>
                    <span className="badge badge-gray">{c.categoria}</span>
                  </div>
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-soft)', lineHeight: 1.5 }}>{c.descricao}</p>
                  {c.frequencia && (
                    <div style={{ marginTop: 6, fontSize: '0.8rem', color: 'var(--moss)', fontWeight: 500 }}>
                      🔁 {c.frequencia}
                    </div>
                  )}
                </div>
                <button className="btn btn-danger btn-sm" onClick={() => del(c.id)}>
                  <Trash2 size={13} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
