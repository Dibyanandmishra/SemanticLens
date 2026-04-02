export const NAV_ITEMS = [
  { id: 'about', label: 'About' },
  { id: 'features', label: 'Features' },
  { id: 'architecture', label: 'Architecture' },
  { id: 'stack', label: 'Tech Stack' },
  { id: 'demo', label: 'Demo' },
  { id: 'highlights', label: 'Highlights' },
  { id: 'contact', label: 'Contact' },
]

export const FEATURES = [
  {
    title: 'Visual Similarity Search',
    description: 'Embeddings capture visual patterns and retrieve nearest matches with high precision.',
  },
  {
    title: 'Semantic Understanding',
    description: 'Caption and language layers interpret intent beyond low-level pixel similarity.',
  },
  {
    title: 'Hybrid Search',
    description: 'Ranking combines visual and textual signals for context-aware result relevance.',
  },
  {
    title: 'Fast Retrieval',
    description: 'Indexed feature vectors support low-latency lookups even at scale.',
  },
  {
    title: 'API Integration',
    description: 'Service-oriented interfaces are designed for easy frontend/backend interoperability.',
  },
]

export const ARCHITECTURE_STEPS = [
  'Image Upload',
  'Embedding Service',
  'Vector Index',
  'Caption Model',
  'Hybrid Ranker',
  'Result API',
]

export const TECH_STACK = [
  { name: 'React', category: 'Frontend' },
  { name: 'Vite', category: 'Build System' },
  { name: 'Framer Motion', category: 'Animation' },
  { name: 'Axios', category: 'HTTP Client' },
  { name: 'Python', category: 'AI Backend' },
  { name: 'FAISS / Vector DB', category: 'Retrieval' },
  { name: 'Transformers', category: 'NLP/Vision' },
  { name: 'REST API', category: 'Integration' },
]

export const HIGHLIGHTS = [
  {
    title: 'System Design Thinking',
    description: 'The architecture separates embedding, indexing, ranking, and API delivery for maintainable evolution.',
  },
  {
    title: 'AI + Backend Integration',
    description: 'Frontend interaction patterns align with asynchronous ML inference and retrieval service contracts.',
  },
  {
    title: 'Scalability Considerations',
    description: 'The pipeline is designed to support caching, sharded indexing, and iterative model upgrades.',
  },
  {
    title: 'Non-CRUD Engineering',
    description: 'This project focuses on multimodal ranking complexity rather than standard form-and-table workflows.',
  },
]
