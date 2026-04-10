import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
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

// ─── ATIVIDADES TAB ────────────────────────────────────────
function AtividadesTab({ petId }) {
  const [atividades, setAtividades] = useState([])
  const [sugestoes, setSugestoes] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    tipo: '', data: '', duracao_minutos: '', distancia_km: '', intensidade: 'moderada', observacoes: '',
  })

  const load = () => {
    Promise.all([atividadesAPI.listByPet(petId), atividadesAPI.sugestoes(petId)])
      .then(([a, s]) => { setAtividades(a.data); setSugestoes(s.data) })
      .finally(() => setLoading(false))
  }
  useEffect(load, [petId])

  const save = async () => {
    if (!form.tipo || !form.data) {
      setError('Tipo e data são obrigatórios.')
      return
    }
    setError('')
    setSaving(true)
    try {
      await atividadesAPI.create({
        ...form,
        pet_id: parseInt(petId),
        duracao_minutos: form.duracao_minutos ? parseInt(form.duracao_minutos) : null,
        distancia_km: form.distancia_km ? parseFloat(form.distancia_km) : null,
      })
      setShowForm(false)
      setForm({ tipo: '', data: '', duracao_minutos: '', distancia_km: '', intensidade: 'moderada', observacoes: '' })
      load()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar atividade.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      {sugestoes && (
        <div className="card" style={{ background: 'var(--moss-pale)', border: 'none', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
            <Lightbulb size={18} style={{ color: 'var(--moss)' }} />
            <strong style={{ color: 'var(--moss)', fontFamily: 'var(--font-display)' }}>
              Sugestões para {sugestoes.pet} — nível {sugestoes.nivel_atividade}
            </strong>
          </div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {sugestoes.sugestoes.map((s, i) => (
              <span key={i} className="badge badge-green" style={{ cursor: 'pointer' }}
                onClick={() => setForm(f => ({ ...f, tipo: s }))}>
                {s}
              </span>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h4 style={{ fontFamily: 'var(--font-display)', color: 'var(--bark)' }}>Atividades Registradas</h4>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowForm(s => !s); setError('') }}>
          {showForm ? <X size={14} /> : <Plus size={14} />} {showForm ? 'Cancelar' : 'Registrar Atividade'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: 20 }}>
          {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Atividade *</label>
              <input className="form-input" value={form.tipo} onChange={e => setForm(f => ({ ...f, tipo: e.target.value }))} placeholder="Ex: Caminhada, Natação..." />
            </div>
            <div className="form-group">
              <label className="form-label">Data *</label>
              <input className="form-input" type="date" value={form.data} onChange={e => setForm(f => ({ ...f, data: e.target.value }))} />
            </div>
          </div>
          <div className="form-row-3">
            <div className="form-group">
              <label className="form-label">Duração (min)</label>
              <input className="form-input" type="number" min="1" value={form.duracao_minutos} onChange={e => setForm(f => ({ ...f, duracao_minutos: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Distância (km)</label>
              <input className="form-input" type="number" step="0.1" min="0" value={form.distancia_km} onChange={e => setForm(f => ({ ...f, distancia_km: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Intensidade</label>
              <select className="form-select" value={form.intensidade} onChange={e => setForm(f => ({ ...f, intensidade: e.target.value }))}>
                <option value="leve">Leve</option>
                <option value="moderada">Moderada</option>
                <option value="intensa">Intensa</option>
              </select>
            </div>
          </div>
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? 'Salvando...' : '🏃 Salvar Atividade'}
          </button>
        </div>
      )}

      {atividades.length === 0 ? (
        <div className="empty-state"><div className="emoji">🏃</div><h3>Nenhuma atividade registrada</h3></div>
      ) : (
        <div className="table-wrap">
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
    </div>
  )
}

// ─── PASSEIOS TAB ──────────────────────────────────────────
function PasseiosTab({ petId }) {
  const [passeios, setPasseios] = useState([])
  const [sugestoes, setSugestoes] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    local: '', data: '', duracao_minutos: '', avaliacao: 5, observacoes: '',
  })

  const load = () => {
    Promise.all([passeiosAPI.listByPet(petId), passeiosAPI.sugestoes(petId)])
      .then(([p, s]) => { setPasseios(p.data); setSugestoes(s.data) })
      .finally(() => setLoading(false))
  }
  useEffect(load, [petId])

  const save = async () => {
    if (!form.local || !form.data) {
      setError('Local e data são obrigatórios.')
      return
    }
    setError('')
    setSaving(true)
    try {
      await passeiosAPI.create({
        ...form,
        pet_id: parseInt(petId),
        duracao_minutos: form.duracao_minutos ? parseInt(form.duracao_minutos) : null,
        avaliacao: parseInt(form.avaliacao),
      })
      setShowForm(false)
      setForm({ local: '', data: '', duracao_minutos: '', avaliacao: 5, observacoes: '' })
      load()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar passeio.')
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      {sugestoes && (
        <div className="card" style={{ background: 'var(--sky-pale)', border: 'none', marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginBottom: 10 }}>
            <MapPin size={18} style={{ color: 'var(--sky)' }} />
            <strong style={{ color: 'var(--sky)', fontFamily: 'var(--font-display)' }}>
              Passeios recomendados — porte {sugestoes.porte}
            </strong>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {sugestoes.sugestoes.map((s, i) => (
              <div key={i} style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
                <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--sky)', cursor: 'pointer' }}
                  onClick={() => setForm(f => ({ ...f, local: s.local }))}>
                  📍 {s.local}
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-soft)' }}>— {s.descricao}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h4 style={{ fontFamily: 'var(--font-display)', color: 'var(--bark)' }}>Passeios Realizados</h4>
        <button className="btn btn-primary btn-sm" onClick={() => { setShowForm(s => !s); setError('') }}>
          {showForm ? <X size={14} /> : <Plus size={14} />} {showForm ? 'Cancelar' : 'Registrar Passeio'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: 20 }}>
          {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Local *</label>
              <input className="form-input" value={form.local} onChange={e => setForm(f => ({ ...f, local: e.target.value }))} placeholder="Ex: Parque Ibirapuera" />
            </div>
            <div className="form-group">
              <label className="form-label">Data *</label>
              <input className="form-input" type="date" value={form.data} onChange={e => setForm(f => ({ ...f, data: e.target.value }))} />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Duração (min)</label>
              <input className="form-input" type="number" min="1" value={form.duracao_minutos} onChange={e => setForm(f => ({ ...f, duracao_minutos: e.target.value }))} />
            </div>
            <div className="form-group">
              <label className="form-label">Avaliação (1-5 ⭐)</label>
              <input className="form-input" type="number" min={1} max={5} value={form.avaliacao} onChange={e => setForm(f => ({ ...f, avaliacao: e.target.value }))} />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Observações</label>
            <textarea className="form-textarea" value={form.observacoes} onChange={e => setForm(f => ({ ...f, observacoes: e.target.value }))} />
          </div>
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? 'Salvando...' : '🗺️ Salvar Passeio'}
          </button>
        </div>
      )}

      {passeios.length === 0 ? (
        <div className="empty-state"><div className="emoji">🗺️</div><h3>Nenhum passeio registrado</h3></div>
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

  useEffect(() => {
    if (!racaId) return setLoading(false)
    cuidadosAPI.listByRaca(racaId, categoria || undefined)
      .then(r => setCuidados(r.data))
      .finally(() => setLoading(false))
  }, [racaId, categoria])

  if (!racaId) return <div className="empty-state"><div className="emoji">🩺</div><h3>Raça não cadastrada</h3></div>
  if (loading) return <div className="spinner" />

  const categorias = ['', 'alimentacao', 'higiene', 'saude', 'comportamento', 'exercicio']
  const prioColor = { alta: 'badge-orange', media: 'badge-blue', baixa: 'badge-gray' }

  return (
    <div>
      <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
        {categorias.map(c => (
          <button key={c} className={`btn btn-sm ${categoria === c ? 'btn-primary' : 'btn-outline'}`}
            onClick={() => setCategoria(c)}>
            {c || 'Todos'}
          </button>
        ))}
      </div>

      {cuidados.length === 0 ? (
        <div className="empty-state"><div className="emoji">🩺</div><h3>Nenhum cuidado cadastrado para esta raça</h3></div>
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
  const [pet, setPet] = useState(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState('vacinas')

  useEffect(() => {
    petsAPI.get(id).then(r => setPet(r.data)).finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="spinner" />
  if (!pet) return <div className="empty-state"><h3>Pet não encontrado</h3></div>

  const tabs = [
    { id: 'vacinas', label: '💉 Vacinas' },
    { id: 'atividades', label: '🏃 Atividades' },
    { id: 'passeios', label: '🗺️ Passeios' },
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
          {tab === 'passeios' && <PasseiosTab petId={id} />}
          {tab === 'cuidados' && <CuidadosTab racaId={pet.raca?.id} />}
        </div>
      </div>
    </div>
  )
}
