import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { PawPrint, Syringe, Dumbbell, MapPin, AlertTriangle, ChevronRight, TrendingUp } from 'lucide-react'
import { petsAPI, vacinasAPI } from '../services/api'
import { format, differenceInDays } from 'date-fns'
import { ptBR } from 'date-fns/locale'

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

export default function Dashboard() {
  const [pets, setPets] = useState([])
  const [pendentes, setPendentes] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    Promise.all([petsAPI.list(), vacinasAPI.pendentes()])
      .then(([pRes, vRes]) => {
        setPets(pRes.data)
        setPendentes(vRes.data)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="spinner" />

  const hoje = new Date()

  return (
    <div>
      <div className="page-header">
        <h2>Olá! Bem-vindo ao PetCare 🐾</h2>
        <p>Acompanhe a saúde e o bem-estar dos seus pets em um só lugar.</p>
      </div>

      {/* Stats */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon moss"><PawPrint size={22} /></div>
          <div>
            <div className="stat-value">{pets.length}</div>
            <div className="stat-label">Pets cadastrados</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon terra"><AlertTriangle size={22} /></div>
          <div>
            <div className="stat-value">{pendentes.length}</div>
            <div className="stat-label">Vacinas pendentes</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon sky"><Syringe size={22} /></div>
          <div>
            <div className="stat-value">∞</div>
            <div className="stat-label">Amor pelos pets</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon sand"><TrendingUp size={22} /></div>
          <div>
            <div className="stat-value">100%</div>
            <div className="stat-label">Dedicação</div>
          </div>
        </div>
      </div>

      {/* Alertas de vacinas */}
      {pendentes.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--bark)', marginBottom: 12 }}>
            ⚠️ Vacinas que precisam de atenção
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {pendentes.slice(0, 5).map(v => {
              const dias = differenceInDays(new Date(v.proxima_dose), hoje)
              return (
                <div key={v.id} className="alert alert-warning">
                  <Syringe size={16} />
                  <span>
                    <strong>{v.nome}</strong> — {dias < 0
                      ? `Atrasada há ${Math.abs(dias)} dias`
                      : `Vence em ${dias} dias`}
                    {v.proxima_dose && ` (${format(new Date(v.proxima_dose), "dd 'de' MMM", { locale: ptBR })})`}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Lista de Pets */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
        <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--bark)' }}>
          Seus Pets
        </h3>
        <button className="btn btn-ghost btn-sm" onClick={() => navigate('/pets')}>
          Ver todos <ChevronRight size={14} />
        </button>
      </div>

      {pets.length === 0 ? (
        <div className="empty-state">
          <div className="emoji">🐾</div>
          <h3>Nenhum pet cadastrado ainda</h3>
          <p>Vá até "Meus Pets" para adicionar seu primeiro companheiro!</p>
        </div>
      ) : (
        <div className="card-grid">
          {pets.slice(0, 6).map(pet => (
            <div key={pet.id} className="pet-card" onClick={() => navigate(`/pets/${pet.id}`)}>
              <div className="pet-card-avatar" style={{ background: getAvatarBg(pet.id) }}>
                <span>{getPetEmoji(pet.raca?.especie, pet.raca?.porte)}</span>
              </div>
              <div className="pet-card-body">
                <div className="pet-card-name">{pet.nome}</div>
                <div className="pet-card-meta">{pet.raca?.nome || 'Raça não informada'}</div>
                <div className="pet-card-tags">
                  {pet.raca?.porte && <span className="badge badge-green">{pet.raca.porte}</span>}
                  {pet.sexo && <span className="badge badge-gray">{pet.sexo}</span>}
                  {pet.peso_kg && <span className="badge badge-blue">{pet.peso_kg} kg</span>}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
