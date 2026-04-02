import MainLayout from './layouts/MainLayout'
import HeroSection from './sections/HeroSection'
import AboutSection from './sections/AboutSection'
import FeaturesSection from './sections/FeaturesSection'
import ArchitectureSection from './sections/ArchitectureSection'
import TechStackSection from './sections/TechStackSection'
import DemoSection from './sections/DemoSection'
import HighlightsSection from './sections/HighlightsSection'
import ContactSection from './sections/ContactSection'

function App() {
  return (
    <MainLayout>
      <HeroSection />
      <AboutSection />
      <FeaturesSection />
      <ArchitectureSection />
      <TechStackSection />
      <DemoSection />
      <HighlightsSection />
      <ContactSection />
    </MainLayout>
  )
}

export default App
