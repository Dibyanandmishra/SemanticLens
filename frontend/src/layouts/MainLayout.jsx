import { useEffect, useMemo, useState } from 'react'
import Navbar from '../components/Navbar'
import { NAV_ITEMS } from '../utils/constants'

function MainLayout({ children }) {
  const sectionIds = useMemo(() => NAV_ITEMS.map((item) => item.id), [])
  const [activeSection, setActiveSection] = useState(sectionIds[0])

  useEffect(() => {
    const updateActiveSection = () => {
      const scrollPosition = window.scrollY + 120
      let current = sectionIds[0]

      sectionIds.forEach((id) => {
        const section = document.getElementById(id)
        if (section && section.offsetTop <= scrollPosition) {
          current = id
        }
      })

      setActiveSection(current)
    }

    updateActiveSection()
    window.addEventListener('scroll', updateActiveSection, { passive: true })

    return () => window.removeEventListener('scroll', updateActiveSection)
  }, [sectionIds])

  return (
    <div className="page-shell">
      <Navbar activeSection={activeSection} items={NAV_ITEMS} />
      <main className="main-content">{children}</main>
    </div>
  )
}

export default MainLayout
