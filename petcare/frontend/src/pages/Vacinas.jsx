import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { vacinasAPI, petsAPI } from '../services/api'
import { format, differenceInDays } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'

export default function Vacinas() {
  const [pendentes, setPendentes] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    vacinasAPI.pendentes().then(r => setPendentes(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="spinner" />

  const hoje = new Date()
  const vencidas = pendentes.filter(v => differenceInDays(new Date(v.proxima_dose), hoje) < 0)
  const proximas = pendentes.filter(v => differenceInDays(new Date(v.proxima_dose), hoje) >= 0)

  return (
    <div>
      <div className="page-header">
        <h2>Controle Vacinal</h2>
        <p>Acompanhe as vacinas pendentes e vencidas de todos os seus pets</p>
      </div>

      <div className="stat-grid" style={{ marginBottom: 32 }}>
        <div className="stat-card">
          <div className="stat-icon terra"><AlertTriangle size={22} /></div>
          <div>
            <div className="stat-value">{vencidas.length}</div>
            <div className="stat-label">Vacinas atrasadas</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon sky"><Clock size={22} /></div>
          <div>
            <div className="stat-value">{proximas.length}</div>
            <div className="stat-label">Vencem em 30 dias</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon moss"><CheckCircle size={22} /></div>
          <div>
            <div className="stat-value">{pendentes.length}</div>
            <div className="stat-label">Total com atenção</div>
          </div>
        </div>
      </div>

      {pendentes.length === 0 ? (
        <div className="empty-state">
          <div className="emoji">✅</div>
          <h3>Tudo em dia!</h3>
          <p>Nenhuma vacina pendente ou próxima do vencimento.</p>
        </div>
      ) : (
        <>
          {vencidas.length > 0 && (
            <div style={{ marginBottom: 28 }}>
              <h3 style={{ fontFamily: 'var(--font-display)', color: '#dc2626', marginBottom: 14, fontSize: '1.05rem' }}>
                ⛔ Vacinas Atrasadas ({vencidas.length})
              </h3>
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Vacina</th><th>Pet ID</th><th>Vencimento</th><th>Atraso</th><th></th></tr></thead>
                  <tbody>
                    {vencidas.map(v => (
                      <tr key={v.id}>
                        <td><strong>{v.nome}</strong></td>
                        <td>Pet #{v.pet_id}</td>
                        <td>{format(new Date(v.proxima_dose), 'dd/MM/yyyy')}</td>
                        <td><span className="badge badge-red">{Math.abs(differenceInDays(new Date(v.proxima_dose), hoje))} dias</span></td>
                        <td><button className="btn btn-outline btn-sm" onClick={() => navigate(`/pets/${v.pet_id}`)}>Ver Pet</button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {proximas.length > 0 && (
            <div>
              <h3 style={{ fontFamily: 'var(--font-display)', color: 'var(--terra)', marginBottom: 14, fontSize: '1.05rem' }}>
                🔔 Próximas do Vencimento ({proximas.length})
              </h3>
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Vacina</th><th>Pet ID</th><th>Data Prevista</th><th>Faltam</th><th></th></tr></thead>
                  <tbody>
                    {proximas.map(v => {
                      const dias = differenceInDays(new Date(v.proxima_dose), hoje)
                      return (
                        <tr key={v.id}>
                          <td><strong>{v.nome}</strong></td>
                          <td>Pet #{v.pet_id}</td>
                          <td>{format(new Date(v.proxima_dose), "dd 'de' MMM", { locale: ptBR })}</td>
                          <td><span className={`badge ${dias <= 7 ? 'badge-orange' : 'badge-blue'}`}>{dias} dias</span></td>
                          <td><button className="btn btn-outline btn-sm" onClick={() => navigate(`/pets/${v.pet_id}`)}>Ver Pet</button></td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
