import { NavLink } from 'react-router-dom'

export default function NavBar() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar__brand">
        Проектирование API
      </NavLink>
      <NavLink to="/theory">Теория</NavLink>
      <NavLink to="/practice">Практика</NavLink>
      <NavLink to="/final-test">Итоговый тест</NavLink>
      <NavLink to="/progress">Прогресс</NavLink>
    </nav>
  )
}
