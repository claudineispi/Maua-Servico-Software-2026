import { useState, useEffect } from 'react'
import { useParams, useNavigate, useSearchParams } from 'react-router-dom'
import { ArrowLeft, Syringe, Dumbbell, MapPin, Heart, Plus, X, Lightbulb } from 'lucide-react'
import { petsAPI, vacinasAPI, atividadesAPI, passeiosAPI, cuidadosAPI } from '../services/api'
import { format, differenceInYears, differenceInMonths, differenceInDays } from 'date-fns'
import { ptBR } from 'date-fns/locale'

// Evita o bug de fuso horário: "2024-01-15" (UTC) → exibe 2024-01-14 em UTC-3
function parseLocalDate(dateStr) {
  if (!dateStr) return new Date()
  const [y, m, d] = dateStr.split('-').map(Number)
  return new Date(y, m - 1, d)
}

function petAge(dateStr) {
  if (!dateStr) return '—'
  const birth = parseLocalDate(dateStr)
  const now = new Date()
  const years = differenceInYears(now, birth)
  if (years >= 1) return `${years} ano${years > 1 ? 's' : ''}`
  const months = differenceInMonths(now, birth)
  if (months >= 1) return `${months} ${months > 1 ? 'meses' : 'mês'}`
  return `${differenceInDays(now, birth)} dias`
}

function getPetEmoji(especie, porte) {
  if (especie === 'gato') return '🐱'
  if (porte === 'grande') return '🐕'
  if (porte === 'pequeno') return '🐩'
  return '🐶'
}

// ─── VACINAS TAB ───────────────────────────────────────────
function VacinasTab({ petId }) {
  const [vacinas, setVacinas] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    nome: '', data_aplicacao: '', proxima_dose: '',
    veterinario: '', clinica: '', lote: '', observacoes: '',
  })

  const load = () =>
    vacinasAPI.listByPet(petId).then(r => setVacinas(r.data)).finally(() => setLoading(false))

  useEffect(load, [petId])

  const save = async () => {
    if (!form.nome || !form.data_aplicacao) {
      setError('Nome e data de aplicação são obrigatórios.')
      return
    }
    setError('')
    setSaving(true)
    try {
      await vacinasAPI.create({
        ...form,
        pet_id: parseInt(petId),
        proxima_dose: form.proxima_dose || null,
      })
      setShowForm(false)
      setForm({ nome: '', data_aplicacao: '', proxima_dose: '', veterinario: '', clinica: '', lote: '', observacoes: '' })
      load()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar vacina.')
    } finally {
      setSaving(false)
    }
  }

  const del = async (id) => {
    if (!confirm('Remover vacina?')) return
    try {
      await vacinasAPI.delete(id)
      load()
    } catch {
      alert('Erro ao remover vacina.')
    }
  }

  const getDotClass = (v) => {
    if (!v.proxima_dose) return ''
    const dias = differenceInDays(parseLocalDate(v.proxima_dose), new Date())
    if (dias < 0) return 'overdue'
    if (dias <= 30) return 'pending'
    return ''
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h4 style={{ fontFamily: 'var(--font-display)', color: 'var(--bark)' }}>Histórico Vacinal</h4>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowForm(s => !s); setError('') }}>
          {showForm ? <X size={14} /> : <Plus size={14} />} {showForm ? 'Cancelar' : 'Registrar Vacina'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: 20, background: 'var(--moss-pale)' }}>
          {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Vacina *</label>
              <input className="form-input" value={form.nome} onChange={e => setForm(f => ({ ...f, nome: e.target.value }))} placeholder="Ex: V10, Antirrábica..." />
            </div>
            <div className="form-group">
              <label className="form-label">Data de Aplicação *</label>
              <input className="form-input" type="date" value={form.data_aplicacao} onChange={e => setForm(f => ({ ...f, data_aplicacao: e.target.value }))} />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Próxima Dose</label>
              <input className="form-input" type="date" value={form.proxima_dose} onChange={e => setForm(f => ({ ...f, proxima_dose: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Veterinário</label>
              <input className="form-input" value={form.veterinario} onChange={e => setForm(f => ({ ...f, veterinario: e.target.value }))} />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Clínica</label>
              <input className="form-input" value={form.clinica} onChange={e => setForm(f => ({ ...f, clinica: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Lote</label>
              <input className="form-input" value={form.lote} onChange={e => setForm(f => ({ ...f, lote: e.target.value }))} />
            </div>
          </div>
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? 'Salvando...' : '💉 Salvar Vacina'}
          </button>
        </div>
      )}

      {vacinas.length === 0 ? (
        <div className="empty-state"><div className="emoji">💉</div><h3>Nenhuma vacina registrada</h3></div>
      ) : (
        <div className="timeline">
          {vacinas.map(v => {
            const dc = getDotClass(v)
            const diasProxima = v.proxima_dose
              ? differenceInDays(parseLocalDate(v.proxima_dose), new Date())
              : null
            return (
              <div key={v.id} className="timeline-item">
                <div className={`timeline-dot ${dc}`} />
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <div style={{ fontWeight: 600, color: 'var(--bark)' }}>{v.nome}</div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-soft)', marginTop: 2 }}>
                      Aplicada em {format(parseLocalDate(v.data_aplicacao), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
                      {v.veterinario && ` • Dr(a). ${v.veterinario}`}
                      {v.clinica && ` • ${v.clinica}`}
                    </div>
                    {v.proxima_dose && (
                      <div style={{ marginTop: 4 }}>
                        {diasProxima < 0
                          ? <span className="badge badge-red">⚠ Atrasada {Math.abs(diasProxima)} dias</span>
                          : diasProxima <= 30
                          ? <span className="badge badge-orange">🔔 Reforço em {diasProxima} dias</span>
                          : <span className="badge badge-green">✓ Próxima: {format(parseLocalDate(v.proxima_dose), 'dd/MM/yyyy')}</span>
                        }
                      </div>
                    )}
                  </div>
                  <button className="btn btn-danger btn-sm" onClick={() => del(v.id)}>Remover</button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ─── ATIVIDADES & PASSEIOS TAB (unificada) ────────────────
function AtividadesTab({ petId }) {
  const [atividades, setAtividades] = useState([])
  const [passeios, setPasseios] = useState([])
  const [sugestoesAtiv, setSugestoesAtiv] = useState(null)
  const [sugestoesPas, setSugestoesPas] = useState(null)
  const [loading, setLoading] = useState(true)

  // Atividade form
  const [showFormAtiv, setShowFormAtiv] = useState(false)
  const [savingAtiv, setSavingAtiv] = useState(false)
  const [errorAtiv, setErrorAtiv] = useState('')
  const [formAtiv, setFormAtiv] = useState({
    tipo: '', data: '', duracao_minutos: '', distancia_km: '', intensidade: 'moderada',
  })

  // Passeio form
  const [showFormPas, setShowFormPas] = useState(false)
  const [savingPas, setSavingPas] = useState(false)
  const [errorPas, setErrorPas] = useState('')
  const [formPas, setFormPas] = useState({
    local: '', data: '', duracao_minutos: '', avaliacao: 5, observacoes: '',
  })

  const load = () => {
    Promise.all([
      atividadesAPI.listByPet(petId),
      atividadesAPI.sugestoes(petId),
      passeiosAPI.listByPet(petId),
      passeiosAPI.sugestoes(petId),
    ])
      .then(([a, sa, p, sp]) => {
        setAtividades(a.data); setSugestoesAtiv(sa.data)
        setPasseios(p.data); setSugestoesPas(sp.data)
      })
      .finally(() => setLoading(false))
  }
  useEffect(load, [petId])

  const saveAtiv = async () => {
    if (!formAtiv.tipo || !formAtiv.data) { setErrorAtiv('Tipo e data são obrigatórios.'); return }
    setErrorAtiv(''); setSavingAtiv(true)
    try {
      await atividadesAPI.create({
        ...formAtiv, pet_id: parseInt(petId),
        duracao_minutos: formAtiv.duracao_minutos ? parseInt(formAtiv.duracao_minutos) : null,
        distancia_km: formAtiv.distancia_km ? parseFloat(formAtiv.distancia_km) : null,
      })
      setShowFormAtiv(false)
      setFormAtiv({ tipo: '', data: '', duracao_minutos: '', distancia_km: '', intensidade: 'moderada' })
      load()
    } catch (e) { setErrorAtiv(e.response?.data?.detail || 'Erro ao salvar atividade.') }
    finally { setSavingAtiv(false) }
  }

  const savePas = async () => {
    if (!formPas.local || !formPas.data) { setErrorPas('Local e data são obrigatórios.'); return }
    setErrorPas(''); setSavingPas(true)
    try {
      await passeiosAPI.create({
        ...formPas, pet_id: parseInt(petId),
        duracao_minutos: formPas.duracao_minutos ? parseInt(formPas.duracao_minutos) : null,
        avaliacao: parseInt(formPas.avaliacao),
      })
      setShowFormPas(false)
      setFormPas({ local: '', data: '', duracao_minutos: '', avaliacao: 5, observacoes: '' })
      load()
    } catch (e) { setErrorPas(e.response?.data?.detail || 'Erro ao salvar passeio.') }
    finally { setSavingPas(false) }
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      {/* ── Sugestões de atividades ── */}
      {sugestoesAtiv && (
        <div className="card" style={{ background: 'var(--moss-pale)', border: 'none', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
            <Lightbulb size={18} style={{ color: 'var(--moss)' }} />
            <strong style={{ color: 'var(--moss)', fontFamily: 'var(--font-display)' }}>
              Sugestões de atividade — nível {sugestoesAtiv.nivel_atividade}
            </strong>
          </div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {sugestoesAtiv.sugestoes.map((s, i) => (
              <span key={i} className="badge badge-green" style={{ cursor: 'pointer' }}
                onClick={() => { setFormAtiv(f => ({ ...f, tipo: s })); setShowFormAtiv(true) }}>
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* ── Sugestões de passeios ── */}
      {sugestoesPas && (
        <div className="card" style={{ background: 'var(--sky-pale)', border: 'none', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
            <MapPin size={18} style={{ color: 'var(--sky)' }} />
            <strong style={{ color: 'var(--sky)', fontFamily: 'var(--font-display)' }}>
              Passeios recomendados — porte {sugestoesPas.porte}
            </strong>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {sugestoesPas.sugestoes.map((s, i) => (
              <div key={i} style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--sky)', cursor: 'pointer' }}
                  onClick={() => { setFormPas(f => ({ ...f, local: s.local })); setShowFormPas(true) }}>
                  📍 {s.local}
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-soft)' }}>— {s.descricao}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ═══════════════ ATIVIDADES ═══════════════ */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h4 style={{ fontFamily: 'var(--font-display)', color: 'var(--bark)' }}>🏃 Atividades</h4>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowFormAtiv(s => !s); setErrorAtiv('') }}>
          {showFormAtiv ? <X size={14} /> : <Plus size={14} />} {showFormAtiv ? 'Cancelar' : 'Nova Atividade'}
        </button>
      </div>

      {showFormAtiv && (
        <div className="card" style={{ marginBottom: 20 }}>
          {errorAtiv && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{errorAtiv}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Atividade *</label>
              <input className="form-input" value={formAtiv.tipo} onChange={e => setFormAtiv(f => ({ ...f, tipo: e.target.value }))} placeholder="Ex: Caminhada, Natação..." />
            </div>
            <div className="form-group">
              <label className="form-label">Data *</label>
              <input className="form-input" type="date" value={formAtiv.data} onChange={e => setFormAtiv(f => ({ ...f, data: e.target.value }))} />
            </div>
          </div>
          <div className="form-row-3">
            <div className="form-group">
              <label className="form-label">Duração (min)</label>
              <input className="form-input" type="number" min="1" value={formAtiv.duracao_minutos} onChange={e => setFormAtiv(f => ({ ...f, duracao_minutos: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Distância (km)</label>
              <input className="form-input" type="number" step="0.1" min="0" value={formAtiv.distancia_km} onChange={e => setFormAtiv(f => ({ ...f, distancia_km: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Intensidade</label>
              <select className="form-select" value={formAtiv.intensidade} onChange={e => setFormAtiv(f => ({ ...f, intensidade: e.target.value }))}>
                <option value="leve">Leve</option>
                <option value="moderada">Moderada</option>
                <option value="intensa">Intensa</option>
              </select>
            </div>
          </div>
          <button className="btn btn-primary" onClick={saveAtiv} disabled={savingAtiv}>
            {savingAtiv ? 'Salvando...' : '🏃 Salvar Atividade'}
          </button>
        </div>
      )}

      {atividades.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '20px 0', color: 'var(--text-soft)', fontSize: '0.9rem' }}>Nenhuma atividade registrada.</div>
      ) : (
        <div className="table-wrap" style={{ marginBottom: 32 }}>
          <table>
            <thead>
              <tr><th>Atividade</th><th>Data</th><th>Duração</th><th>Distância</th><th>Intensidade</th><th></th></tr>
            </thead>
            <tbody>
              {atividades.map(a => (
                <tr key={a.id}>
                  <td><strong>{a.tipo}</strong></td>
                  <td>{format(parseLocalDate(a.data), 'dd/MM/yyyy')}</td>
                  <td>{a.duracao_minutos ? `${a.duracao_minutos} min` : '—'}</td>
                  <td>{a.distancia_km ? `${a.distancia_km} km` : '—'}</td>
                  <td>
                    <span className={`badge ${a.intensidade === 'intensa' ? 'badge-orange' : a.intensidade === 'moderada' ? 'badge-blue' : 'badge-gray'}`}>
                      {a.intensidade || '—'}
                    </span>
                  </td>
                  <td>
                    <button className="btn btn-ghost btn-sm" onClick={async () => {
                      if (!confirm('Remover?')) return
                      try { await atividadesAPI.delete(a.id); load() } catch { alert('Erro ao remover.') }
                    }}>✕</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ═══════════════ PASSEIOS ═══════════════ */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h4 style={{ fontFamily: 'var(--font-display)', color: 'var(--bark)' }}>🗺️ Passeios</h4>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowFormPas(s => !s); setErrorPas('') }}>
          {showFormPas ? <X size={14} /> : <Plus size={14} />} {showFormPas ? 'Cancelar' : 'Novo Passeio'}
        </button>
      </div>

      {showFormPas && (
        <div className="card" style={{ marginBottom: 20 }}>
          {errorPas && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{errorPas}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Local *</label>
              <input className="form-input" value={formPas.local} onChange={e => setFormPas(f => ({ ...f, local: e.target.value }))} placeholder="Ex: Parque Ibirapuera" />
            </div>
            <div className="form-group">
              <label className="form-label">Data *</label>
              <input className="form-input" type="date" value={formPas.data} onChange={e => setFormPas(f => ({ ...f, data: e.target.value }))} />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Duração (min)</label>
              <input className="form-input" type="number" min="1" value={formPas.duracao_minutos} onChange={e => setFormPas(f => ({ ...f, duracao_minutos: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Avaliação (1-5 ⭐)</label>
              <input className="form-input" type="number" min={1} max={5} value={formPas.avaliacao} onChange={e => setFormPas(f => ({ ...f, avaliacao: e.target.value }))} />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Observações</label>
            <textarea className="form-textarea" value={formPas.observacoes} onChange={e => setFormPas(f => ({ ...f, observacoes: e.target.value }))} />
          </div>
          <button className="btn btn-primary" onClick={savePas} disabled={savingPas}>
            {savingPas ? 'Salvando...' : '🗺️ Salvar Passeio'}
          </button>
        </div>
      )}

      {passeios.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '20px 0', color: 'var(--text-soft)', fontSize: '0.9rem' }}>Nenhum passeio registrado.</div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {passeios.map(p => (
            <div key={p.id} className="card" style={{ padding: '16px 20px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontWeight: 600, color: 'var(--bark)', fontSize: '1rem' }}>📍 {p.local}</div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-soft)', marginTop: 2 }}>
                    {format(parseLocalDate(p.data), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
                    {p.duracao_minutos && ` • ${p.duracao_minutos} min`}
                  </div>
                  {p.avaliacao && (
                    <div className="stars" style={{ marginTop: 6 }}>
                      {[1, 2, 3, 4, 5].map(s => (
                        <span key={s} className={`star ${s <= p.avaliacao ? 'filled' : ''}`}>★</span>
                      ))}
                    </div>
                  )}
                  {p.observacoes && (
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-soft)', marginTop: 4 }}>{p.observacoes}</div>
                  )}
                </div>
                <button className="btn btn-ghost btn-sm" onClick={async () => {
                  if (!confirm('Remover?')) return
                  try { await passeiosAPI.delete(p.id); load() } catch { alert('Erro ao remover.') }
                }}>✕</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── CUIDADOS TAB ──────────────────────────────────────────
function CuidadosTab({ racaId }) {
  const [cuidados, setCuidados] = useState([])
  const [loading, setLoading] = useState(true)
  const [categoria, setCategoria] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    categoria: 'alimentacao', titulo: '', descricao: '', frequencia: '', prioridade: 'media',
  })

  const categorias = ['', 'alimentacao', 'higiene', 'saude', 'comportamento', 'exercicio']
  const prioColor = { alta: 'badge-orange', media: 'badge-blue', baixa: 'badge-gray' }

  const load = () => {
    if (!racaId) return setLoading(false)
    cuidadosAPI.listByRaca(racaId, categoria || undefined)
      .then(r => setCuidados(r.data))
      .finally(() => setLoading(false))
  }

  useEffect(load, [racaId, categoria])

  const save = async () => {
    if (!form.titulo || !form.descricao) {
      setError('Titulo e descricao sao obrigatorios.')
      return
    }
    setError('')
    setSaving(true)
    try {
      await cuidadosAPI.create({
        ...form,
        raca_id: racaId,
        frequencia: form.frequencia || null,
      })
      setShowForm(false)
      setForm({ categoria: 'alimentacao', titulo: '', descricao: '', frequencia: '', prioridade: 'media' })
      load()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar cuidado.')
    } finally {
      setSaving(false)
    }
  }

  const del = async (id) => {
    if (!confirm('Remover este cuidado?')) return
    try { await cuidadosAPI.delete(id); load() } catch { alert('Erro ao remover.') }
  }

  if (!racaId) return <div className="empty-state"><div className="emoji">🩺</div><h3>Raca nao cadastrada</h3></div>
  if (loading) return <div className="spinner" />

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, flexWrap: 'wrap', gap: 10 }}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {categorias.map(c => (
            <button key={c} className={`btn btn-sm ${categoria === c ? 'btn-primary' : 'btn-outline'}`}
              onClick={() => setCategoria(c)}>
              {c || 'Todos'}
            </button>
          ))}
        </div>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowForm(s => !s); setError('') }}>
          {showForm ? <X size={14} /> : <Plus size={14} />} {showForm ? 'Cancelar' : 'Novo Cuidado'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: 20, background: 'var(--moss-pale)' }}>
          {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Categoria *</label>
              <select className="form-select" value={form.categoria} onChange={e => setForm(f => ({ ...f, categoria: e.target.value }))}>
                {categorias.filter(c => c).map(c => <option key={c} value={c}>{c}</option>)}
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

      {cuidados.length === 0 ? (
        <div className="empty-state"><div className="emoji">🩺</div><h3>Nenhum cuidado cadastrado para esta raca</h3><p>Clique em "Novo Cuidado" para adicionar.</p></div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {cuidados.map(c => (
            <div key={c.id} className="card" style={{ padding: '18px 22px' }}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start', justifyContent: 'space-between' }}>
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
                <button className="btn btn-danger btn-sm" onClick={() => del(c.id)}>Remover</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ─── MAIN PAGE ─────────────────────────────────────────────
export default function PetDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [pet, setPet] = useState(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState(searchParams.get('tab') || 'vacinas')

  // Sincroniza a aba com a URL quando o query param muda
  useEffect(() => {
    const tabParam = searchParams.get('tab')
    if (tabParam) setTab(tabParam)
  }, [searchParams])

  useEffect(() => {
    petsAPI.get(id).then(r => setPet(r.data)).finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="spinner" />
  if (!pet) return <div className="empty-state"><h3>Pet não encontrado</h3></div>

  const tabs = [
    { id: 'vacinas', label: '💉 Vacinas' },
    { id: 'atividades', label: '🏃 Atividades & Passeios' },
    { id: 'cuidados', label: '🩺 Cuidados' },
  ]

  return (
    <div>
      <button className="btn btn-ghost btn-sm" style={{ marginBottom: 20 }} onClick={() => navigate(-1)}>
        <ArrowLeft size={15} /> Voltar
      </button>

      {/* Pet Header Card */}
      <div className="card" style={{ marginBottom: 28, display: 'flex', gap: 24, alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{
          width: 80, height: 80, borderRadius: '50%',
          background: 'var(--moss-pale)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2.5rem', flexShrink: 0,
        }}>
          {getPetEmoji(pet.raca?.especie, pet.raca?.porte)}
        </div>
        <div style={{ flex: 1 }}>
          <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.8rem', color: 'var(--bark)' }}>{pet.nome}</h2>
          <div style={{ color: 'var(--text-soft)', fontSize: '0.9rem', marginTop: 2 }}>
            {pet.raca?.nome} • {petAge(pet.data_nascimento)} • {pet.sexo}
            {pet.peso_kg && ` • ${pet.peso_kg} kg`}
            {pet.cor && ` • ${pet.cor}`}
          </div>
          <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
            {pet.raca?.porte && <span className="badge badge-green">{pet.raca.porte}</span>}
            {pet.raca?.especie && <span className="badge badge-gray">{pet.raca.especie}</span>}
            {pet.raca?.nivel_atividade && <span className="badge badge-blue">atividade: {pet.raca.nivel_atividade}</span>}
            {pet.microchip && <span className="badge badge-gray">chip: {pet.microchip}</span>}
          </div>
          {pet.observacoes && (
            <div style={{ marginTop: 10, padding: '8px 12px', background: 'var(--sand)', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem', color: 'var(--text-soft)' }}>
              📝 {pet.observacoes}
            </div>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <div className="tabs" style={{ padding: '0 24px', background: 'var(--cream)', margin: 0 }}>
          {tabs.map(t => (
            <button key={t.id} className={`tab-btn ${tab === t.id ? 'active' : ''}`} onClick={() => setTab(t.id)}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 28 }}>
          {tab === 'vacinas' && <VacinasTab petId={id} />}
          {tab === 'atividades' && <AtividadesTab petId={id} />}
          {tab === 'cuidados' && <CuidadosTab racaId={pet.raca?.id} />}
        </div>
      </div>
    </div>
  )
}
