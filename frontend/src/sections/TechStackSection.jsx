import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'
import { TECH_STACK } from '../utils/constants'

function TechStackSection() {
  return (
    <section id="stack" className="section section-soft">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="Technology Stack"
            title="Tools selected for scale, iteration speed, and maintainability"
            description="Each layer is intentionally selected to support product-grade AI experience delivery."
          />
        </Reveal>
        <div className="stack-grid">
          {TECH_STACK.map((item, index) => (
            <Reveal key={item.name} delay={index * 0.05}>
              <div className="stack-badge">
                <span>{item.name}</span>
                <small>{item.category}</small>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

export default TechStackSection
