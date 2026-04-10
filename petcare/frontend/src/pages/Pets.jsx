import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Search, PawPrint, X } from 'lucide-react'
import { petsAPI, racasAPI, API_URL } from '../services/api'

function getPetEmoji(especie, porte) {
  if (especie === 'gato') return '🐱'
  if (porte === 'grande') return '🐕'
  if (porte === 'pequeno') return '🐩'
  return '🐶'
}

function getAvatarBg(id) {
  const colors = ['#e8f0e4', '#faeee7', '#e4f0f6', '#f5f0e8', '#fef3c7']
  return colors[id % colors.length]
}

function PetModal({ onClose, onSave, racas }) {
  const [form, setForm] = useState({
    nome: '', raca_id: '', data_nascimento: '', sexo: 'macho',
    peso_kg: '', cor: '', microchip: '', observacoes: '',
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [photoFile, setPhotoFile] = useState(null)
  const [photoPreview, setPhotoPreview] = useState(null)

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const handlePhoto = (e) => {
    const file = e.target.files[0]
    if (!file) return
    if (file.size > 5 * 1024 * 1024) {
      setError('A foto deve ter no maximo 5 MB.')
      return
    }
    setPhotoFile(file)
    setPhotoPreview(URL.createObjectURL(file))
  }

  const submit = async () => {
    if (!form.nome || !form.raca_id || !form.data_nascimento) {
      setError('Preencha os campos obrigatórios: Nome, Raça e Data de Nascimento.')
      return
    }
    setError('')
    setSaving(true)
    try {
      const payload = {
        ...form,
        raca_id: parseInt(form.raca_id),
        peso_kg: form.peso_kg ? parseFloat(form.peso_kg) : null,
        microchip: form.microchip || null,
      }
      const res = await petsAPI.create(payload)
      if (photoFile) {
        await petsAPI.uploadPhoto(res.data.id, photoFile)
      }
      onSave()
    } catch (e) {
      setError(e.response?.data?.detail || 'Erro ao salvar pet.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h3>🐾 Novo Pet</h3>
          <button className="btn btn-ghost btn-sm" onClick={onClose}><X size={18} /></button>
        </div>
        {error && <div className="alert alert-warning" style={{ marginBottom: 12 }}>{error}</div>}

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Nome *</label>
            <input className="form-input" name="nome" value={form.nome} onChange={handle} placeholder="Ex: Rex" />
          </div>
          <div className="form-group">
            <label className="form-label">Raça *</label>
            <select className="form-select" name="raca_id" value={form.raca_id} onChange={handle}>
              <option value="">Selecione...</option>
              {racas.map(r => <option key={r.id} value={r.id}>{r.nome}</option>)}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Data de Nascimento *</label>
            <input className="form-input" type="date" name="data_nascimento" value={form.data_nascimento} onChange={handle} />
          </div>
          <div className="form-group">
            <label className="form-label">Sexo</label>
            <select className="form-select" name="sexo" value={form.sexo} onChange={handle}>
              <option value="macho">Macho</option>
              <option value="femea">Fêmea</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Peso (kg)</label>
            <input className="form-input" type="number" step="0.1" name="peso_kg" value={form.peso_kg} onChange={handle} placeholder="Ex: 8.5" />
          </div>
          <div className="form-group">
            <label className="form-label">Cor / Pelagem</label>
            <input className="form-input" name="cor" value={form.cor} onChange={handle} placeholder="Ex: Dourado" />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Microchip</label>
          <input className="form-input" name="microchip" value={form.microchip} onChange={handle} placeholder="Número do microchip" />
        </div>

        <div className="form-group">
          <label className="form-label">Foto do Pet</label>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handlePhoto}
              style={{ fontSize: '0.85rem' }} />
            {photoPreview && (
              <div style={{ position: 'relative' }}>
                <img src={photoPreview} alt="Preview"
                  style={{ width: 64, height: 64, borderRadius: '50%', objectFit: 'cover', border: '2px solid var(--moss-pale)' }} />
                <button type="button" className="btn btn-ghost btn-sm"
                  style={{ position: 'absolute', top: -6, right: -6, padding: 0, width: 20, height: 20, borderRadius: '50%', background: 'var(--bark)', color: 'white', fontSize: '0.7rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                  onClick={() => { setPhotoFile(null); setPhotoPreview(null) }}>
                  ✕
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Observações</label>
          <textarea className="form-textarea" name="observacoes" value={form.observacoes} onChange={handle} placeholder="Alergias, comportamento, informações especiais..." />
        </div>

        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end', marginTop: 8 }}>
          <button className="btn btn-outline" onClick={onClose}>Cancelar</button>
          <button className="btn btn-primary" onClick={submit} disabled={saving}>
            {saving ? 'Salvando...' : '✓ Salvar Pet'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function Pets() {
  const [pets, setPets] = useState([])
  const [racas, setRacas] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [showModal, setShowModal] = useState(false)
  const navigate = useNavigate()

  const load = () => {
    setLoading(true)
    Promise.all([petsAPI.list(), racasAPI.list()])
      .then(([p, r]) => { setPets(p.data); setRacas(r.data) })
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const filtered = pets.filter(p =>
    p.nome.toLowerCase().includes(search.toLowerCase()) ||
    (p.raca?.nome || '').toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <div className="page-header">
        <h2>Meus Pets</h2>
        <p>Gerencie todos os seus animais de estimação</p>
      </div>

      <div style={{ display: 'flex', gap: 12, marginBottom: 28, alignItems: 'center' }}>
        <div style={{ position: 'relative', flex: 1, maxWidth: 340 }}>
          <Search size={16} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text-soft)' }} />
          <input
            className="form-input"
            style={{ paddingLeft: 36 }}
            placeholder="Buscar por nome ou raça..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={16} /> Novo Pet
        </button>
      </div>

      {loading ? <div className="spinner" /> : (
        filtered.length === 0 ? (
          <div className="empty-state">
            <div className="emoji">🐾</div>
            <h3>{search ? 'Nenhum pet encontrado' : 'Nenhum pet cadastrado ainda'}</h3>
            <p>{search ? 'Tente outro termo de busca.' : 'Clique em "Novo Pet" para começar!'}</p>
            {!search && <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setShowModal(true)}><Plus size={16} /> Adicionar Pet</button>}
          </div>
        ) : (
          <div className="card-grid">
            {filtered.map(pet => (
              <div key={pet.id} className="pet-card" onClick={() => navigate(`/pets/${pet.id}`)}>
                <div className="pet-card-avatar" style={{ background: getAvatarBg(pet.id), overflow: 'hidden' }}>
                  {pet.foto_url ? (
                    <img src={`${API_URL}${pet.foto_url}`} alt={pet.nome}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  ) : (
                    <span>{getPetEmoji(pet.raca?.especie, pet.raca?.porte)}</span>
                  )}
                </div>
                <div className="pet-card-body">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div className="pet-card-name">{pet.nome}</div>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-soft)' }}>#{pet.id}</span>
                  </div>
                  <div className="pet-card-meta">{pet.raca?.nome || '—'}</div>
                  {pet.observacoes && (
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-soft)', marginTop: 6, lineHeight: 1.4 }}>
                      {pet.observacoes.slice(0, 60)}{pet.observacoes.length > 60 ? '...' : ''}
                    </div>
                  )}
                  <div className="pet-card-tags">
                    {pet.raca?.porte && <span className="badge badge-green">{pet.raca.porte}</span>}
                    {pet.raca?.especie && <span className="badge badge-gray">{pet.raca.especie}</span>}
                    {pet.peso_kg && <span className="badge badge-blue">{pet.peso_kg} kg</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      {showModal && <PetModal racas={racas} onClose={() => setShowModal(false)} onSave={() => { setShowModal(false); load() }} />}
    </div>
  )
}
