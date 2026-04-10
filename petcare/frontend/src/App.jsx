import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Home, PawPrint, Syringe, Dumbbell, Heart } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Pets from './pages/Pets'
import PetDetail from './pages/PetDetail'
import Vacinas from './pages/Vacinas'
import Atividades from './pages/Atividades'
import Cuidados from './pages/Cuidados'

function Sidebar() {
  const navItems = [
    { to: '/', icon: <Home size={17} />, label: 'Dashboard', exact: true },
    { to: '/pets', icon: <PawPrint size={17} />, label: 'Meus Pets' },
    { to: '/vacinas', icon: <Syringe size={17} />, label: 'Vacinas' },
    { to: '/atividades', icon: <Dumbbell size={17} />, label: 'Atividades' },
    { to: '/cuidados', icon: <Heart size={17} />, label: 'Cuidados' },
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>🐾 PetCare</h1>
        <span>Manager</span>
      </div>
      <nav className="sidebar-nav">
        <div className="nav-section-label">Menu</div>
        {navItems.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.exact}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            {item.icon}
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div style={{ padding: '20px 24px', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Heart size={14} style={{ color: 'var(--terra-light)' }} />
          <span style={{ fontSize: '0.72rem', color: 'rgba(245,240,232,0.35)', fontFamily: 'var(--font-body)' }}>
            Feito com amor pelos pets
          </span>
        </div>
      </div>
    </aside>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/pets" element={<Pets />} />
            <Route path="/pets/:id" element={<PetDetail />} />
            <Route path="/vacinas" element={<Vacinas />} />
            <Route path="/atividades" element={<Atividades />} />
            <Route path="/cuidados" element={<Cuidados />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
