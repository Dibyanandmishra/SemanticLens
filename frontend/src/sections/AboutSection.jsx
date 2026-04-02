import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'

function AboutSection() {
  return (
    <section id="about" className="section">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="About The System"
            title="A retrieval engine built for visual context and semantic intent"
            description="This project is engineered as a real product pipeline: uploaded images are encoded into embeddings, matched against indexed vectors, captioned for semantic context, and ranked through a hybrid scoring strategy to return materially better search outcomes."
          />
        </Reveal>
        <Reveal delay={0.1}>
          <div className="about-flow">
            <span>Image Input</span>
            <span>Feature Extraction</span>
            <span>Similarity Search</span>
            <span>Semantic Captioning</span>
            <span>Hybrid Ranking</span>
          </div>
        </Reveal>
      </div>
    </section>
  )
}

export default AboutSection
