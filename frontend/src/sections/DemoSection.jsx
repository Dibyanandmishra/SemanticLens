import { useState } from 'react'
import Reveal from '../components/Reveal'
import SectionHeading from '../components/SectionHeading'
import { apiClient, searchByImage, searchHybrid } from '../utils/api'

function DemoSection() {
  const [query, setQuery] = useState('green mountain trail with light fog')
  const [selectedFile, setSelectedFile] = useState(null)
  const [results, setResults] = useState([])
  const [caption, setCaption] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const handleDemoSearch = async () => {
    setErrorMessage('')
    console.log('[UI] starting hybrid search', { query, hasFile: Boolean(selectedFile) })
    setIsLoading(true)

    try {
      let payload = null

      if (!selectedFile) {
        setErrorMessage('Please upload an image to run visual search.')
        return
      }

      if (query.trim()) {
        payload = await searchHybrid({ file: selectedFile, query: query.trim() })
      } else {
        payload = await searchByImage({ file: selectedFile })
      }

      const imagePaths = payload?.images || []
      const normalized = imagePaths.map((path) => {
        const cleanPath = String(path || '').replace(/^\/+/, '')
        return `${apiClient.defaults.baseURL}/${cleanPath}`
      })

      console.log('[UI] search completed', { resultCount: normalized.length })
      setCaption(payload?.caption || '')
      setResults(normalized)
    } catch (error) {
      const isTimeout = error.code === 'ECONNABORTED' || String(error.message || '').includes('timeout')
      const message =
        isTimeout
          ? 'Search is taking longer than expected. Please wait and retry.'
          :
        error.response?.data?.detail ||
        'Search failed. Verify backend is running and VITE_API_URL is set correctly.'
      console.error('[UI] search failed', message)
      setErrorMessage(String(message))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section id="demo" className="section">
      <div className="container">
        <Reveal>
          <SectionHeading
            eyebrow="Product Demo Preview"
            title="Search using image context and natural language intent"
            description="A mock interface representing the production UX for hybrid multimodal retrieval."
          />
        </Reveal>
        <Reveal delay={0.08}>
          <div className="demo-shell">
            <div className="demo-controls">
              <label htmlFor="query-input">Semantic query</label>
              <input
                id="query-input"
                type="text"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
              />
              <label htmlFor="file-input">Upload image</label>
              <input
                id="file-input"
                type="file"
                accept="image/*"
                onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
              />
              <div className="demo-button-row">
                <button className="btn btn-primary" type="button" onClick={handleDemoSearch} disabled={isLoading}>
                  {isLoading ? 'Searching...' : 'Run Hybrid Search'}
                </button>
              </div>
              {errorMessage ? <p className="demo-error">{errorMessage}</p> : null}
              {caption ? <p className="demo-caption">Caption: {caption}</p> : null}
            </div>
            <div className="results-grid">
              {results.length > 0 ? (
                results.map((imageUrl) => (
                  <div key={imageUrl} className="result-card">
                    <img className="result-image" src={imageUrl} alt="Similar search result" loading="lazy" />
                    <p>{imageUrl.split('/').at(-1)}</p>
                  </div>
                ))
              ) : (
                <p className="demo-empty">No similar images found</p>
              )}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  )
}

export default DemoSection
