import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'
import { HIGHLIGHTS } from '../utils/constants'

function HighlightsSection() {
  return (
    <section id="highlights" className="section section-soft">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="Project Highlights"
            title="Engineered beyond CRUD into applied AI system design"
            description="The work demonstrates architecture-level thinking across model capabilities, backend orchestration, and front-end product experience."
          />
        </Reveal>
        <div className="highlight-grid">
          {HIGHLIGHTS.map((item, index) => (
            <Reveal key={item.title} delay={index * 0.06}>
              <article className="highlight-card">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}

export default HighlightsSection
