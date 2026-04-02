function Navbar({ items, activeSection }) {
  return (
    <header className="navbar-wrap">
      <nav className="navbar container">
        <a href="#hero" className="brand">
          SemanticLens
        </a>
        <ul className="nav-links">
          {items.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                className={activeSection === item.id ? 'nav-link active' : 'nav-link'}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  )
}

export default Navbar
