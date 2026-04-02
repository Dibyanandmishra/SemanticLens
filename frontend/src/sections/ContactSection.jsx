import Reveal from '../components/Reveal'

function ContactSection() {
  return (
    <section id="contact" className="section contact-section">
      <div className="container">
        <Reveal>
          <div className="contact-card">
            <p className="eyebrow">Contact</p>
            <h2>Dibyanand Mishra</h2>
            <div className="contact-details">
              <p>Phone: 8420253062</p>
              <p>Address: Madhyamgram, Kolkata - 700155</p>
              <a href="mailto:dibyanandmishra@gmail.com">Email: dibyanandmishra@gmail.com</a>
            </div>
            <div className="social-links">
              <a href="https://www.linkedin.com/in/dibyanand-mishra-84865a301/" target="_blank" rel="noreferrer">
                LinkedIn
              </a>
              <a href="https://x.com/nand_dibya51757" target="_blank" rel="noreferrer">
                Twitter
              </a>
              <a href="https://github.com/Dibyanandmishra" target="_blank" rel="noreferrer">
                GitHub
              </a>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}

export default ContactSection
