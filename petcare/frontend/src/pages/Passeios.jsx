import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { petsAPI } from '../services/api'
import { MapPin } from 'lucide-react'

export default function Passeios() {
  const [pets, setPets] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    petsAPI.list().then(r => setPets(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="spinner" />

  return (
    <div>
      <div className="page-header">
        <h2>Passeios</h2>
        <p>Explore os melhores locais e registre as aventuras dos seus pets</p>
      </div>

      {pets.length === 0 ? (
        <div className="empty-state">
          <div className="emoji">🗺️</div>
          <h3>Nenhum pet cadastrado</h3>
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/pets')}>
            Ir para Pets
          </button>
        </div>
      ) : (
        <>
          <div className="alert alert-success" style={{ marginBottom: 24 }}>
            <MapPin size={16} />
            <span>Cada pet recebe sugestões de passeio personalizadas conforme seu porte e energia.</span>
          </div>
          <div className="card-grid">
            {pets.map(pet => (
              <div key={pet.id} className="card" style={{ cursor: 'pointer' }} onClick={() => navigate(`/pets/${pet.id}`)}>
                <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
                  <div style={{ fontSize: '2rem' }}>
                    {pet.raca?.especie === 'gato' ? '🐱' : pet.raca?.porte === 'grande' ? '🐕' : '🐶'}
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, color: 'var(--bark)', fontFamily: 'var(--font-display)' }}>{pet.nome}</div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-soft)' }}>{pet.raca?.nome || '—'}</div>
                    {pet.raca?.porte && <span className="badge badge-green" style={{ marginTop: 6 }}>{pet.raca.porte}</span>}
                  </div>
                </div>
                <div style={{ marginTop: 14 }}>
                  <button className="btn btn-primary btn-sm" onClick={e => { e.stopPropagation(); navigate(`/pets/${pet.id}`) }}>
                    <MapPin size={13} /> Ver Passeios
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
