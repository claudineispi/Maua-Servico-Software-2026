import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { petsAPI, atividadesAPI } from '../services/api'
import { Dumbbell, TrendingUp } from 'lucide-react'

export default function Atividades() {
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
        <h2>Atividades Físicas</h2>
        <p>Acompanhe a saúde e o condicionamento dos seus pets</p>
      </div>

      {pets.length === 0 ? (
        <div className="empty-state">
          <div className="emoji">🏃</div>
          <h3>Nenhum pet cadastrado</h3>
          <p>Cadastre um pet para começar a registrar atividades.</p>
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/pets')}>
            Ir para Pets
          </button>
        </div>
      ) : (
        <>
          <div className="alert alert-success" style={{ marginBottom: 24 }}>
            <TrendingUp size={16} />
            <span>Selecione um pet abaixo para ver e registrar suas atividades com sugestões personalizadas por raça.</span>
          </div>
          <div className="card-grid">
            {pets.map(pet => (
              <div key={pet.id} className="card" style={{ cursor: 'pointer' }}
                onClick={() => navigate(`/pets/${pet.id}?tab=atividades`)}>
                <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
                  <div style={{ fontSize: '2rem' }}>
                    {pet.raca?.especie === 'gato' ? '🐱' : pet.raca?.porte === 'grande' ? '🐕' : '🐶'}
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, color: 'var(--bark)', fontFamily: 'var(--font-display)' }}>{pet.nome}</div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-soft)' }}>{pet.raca?.nome || '—'}</div>
                    {pet.raca?.nivel_atividade && (
                      <span className={`badge ${pet.raca.nivel_atividade === 'alto' ? 'badge-orange' : pet.raca.nivel_atividade === 'medio' ? 'badge-blue' : 'badge-gray'}`} style={{ marginTop: 6 }}>
                        nível {pet.raca.nivel_atividade}
                      </span>
                    )}
                  </div>
                </div>
                <div style={{ marginTop: 14 }}>
                  <button className="btn btn-primary btn-sm" onClick={e => { e.stopPropagation(); navigate(`/pets/${pet.id}`) }}>
                    <Dumbbell size={13} /> Ver Atividades
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
