# DataSanity

An AI-powered web application for dataset cleaning, synthetic data generation, vectorization, and data enrichment using natural language prompts.

## Features
- Dataset cleaning with LLM detection of noisy, missing, or duplicate values
- Synthetic data generation based on schema or prompt
- Vectorization for RAG pipelines
- Data enrichment using web search APIs
- Natural language prompt-based workflow
- Support for CSV uploads and downloads

## Tech Stack
- Frontend: Next.js with Tailwind CSS
- Backend: FastAPI (Python)
- LLM Inference: Cerebras API
- Data Processing: pandas, numpy
- Embedding: sentence-transformers
- Vector Store: FAISS
- Web Search: Exa or Serper.dev
- Storage: SQLite + local filesystem
