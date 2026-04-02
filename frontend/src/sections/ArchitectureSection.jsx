import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'
import { ARCHITECTURE_STEPS } from '../utils/constants'

function ArchitectureSection() {
  return (
    <section id="architecture" className="section">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="Architecture"
            title="Pipeline from ingestion to ranked retrieval"
            description="A modular architecture designed to keep model logic, indexing, and ranking independently scalable."
          />
        </Reveal>
        <Reveal delay={0.08}>
          <div className="architecture-flow">
            {ARCHITECTURE_STEPS.map((step, index) => (
              <div className="flow-node-wrap" key={step}>
                <div className="flow-node">{step}</div>
                {index !== ARCHITECTURE_STEPS.length - 1 ? <div className="flow-arrow">→</div> : null}
              </div>
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  )
}

export default ArchitectureSection
