import { motion } from 'framer-motion'

function HeroSection() {
  const MotionDiv = motion.div

  return (
    <section id="hero" className="hero-section section">
      <div className="container hero-grid">
        <div>
          <p className="eyebrow">AI Project Portfolio</p>
          <h1>AI-Powered Visual Search Engine with Semantic Understanding</h1>
          <p className="hero-copy">
            Search images intelligently using AI-powered visual and semantic understanding.
            Designed for high-confidence retrieval where meaning and appearance both matter.
          </p>
          <div className="hero-actions">
            <a className="btn btn-primary" href="#demo">
              View Demo
            </a>
            <a className="btn btn-secondary" href="https://github.com/Dibyanandmishra" target="_blank" rel="noreferrer">
              View GitHub
            </a>
          </div>
        </div>
        <MotionDiv
          className="hero-visual"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: 'easeOut' }}
        >
          <div className="orb orb-main" />
          <div className="orb orb-sub" />
          <div className="grid-overlay" />
          <div className="visual-card">
            <p>Visual + Semantic Query</p>
            <h3>Hybrid Ranked Results</h3>
          </div>
        </MotionDiv>
      </div>
    </section>
  )
}

export default HeroSection
