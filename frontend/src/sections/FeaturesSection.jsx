import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'
import { FEATURES } from '../utils/constants'

function FeaturesSection() {
  return (
    <section id="features" className="section section-soft">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="Core Features"
            title="Built for practical AI search use-cases"
            description="The platform combines retrieval speed, language understanding, and integration readiness for production workflows."
          />
        </Reveal>
        <div className="feature-grid">
          {FEATURES.map((feature, index) => (
            <Reveal key={feature.title} delay={index * 0.06}>
              <article className="feature-card">
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection
