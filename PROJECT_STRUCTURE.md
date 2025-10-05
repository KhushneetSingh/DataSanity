# DataSanity Project Structure

## Overall Directory Structure

```
DataSanity/
├── README.md
├── SETUP.md
├── PROJECT_STRUCTURE.md
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── pages/
│   │   └── index.js
│   ├── components/
│   │   ├── DataTable.js
│   │   └── DownloadButtons.js
│   └── public/
│       └── favicon.ico
└── backend/
    ├── requirements.txt
    ├── main.py
    ├── cerebras_client.py
    ├── routes/
    │   ├── clean.py
    │   ├── generate.py
    │   ├── embed.py
    │   ├── enrich.py
    │   └── download.py
    └── prompts/
        ├── clean_template.txt
        ├── generate_template.txt
        ├── embed_template.txt
        └── enrich_template.txt
```

## Frontend Structure

### Configuration Files
- `package.json`: Project dependencies and scripts
- `next.config.js`: Next.js configuration
- `postcss.config.js`: PostCSS configuration for Tailwind CSS
- `tailwind.config.js`: Tailwind CSS configuration

### Pages
- `pages/index.js`: Main application page with user interface

### Components
- `components/DataTable.js`: Component for displaying data in table format
- `components/DownloadButtons.js`: Component with buttons for downloading processed data

### Public Assets
- `public/favicon.ico`: Application favicon

## Backend Structure

### Configuration Files
- `requirements.txt`: Python dependencies
- `main.py`: Main FastAPI application file

### Core Modules
- `cerebras_client.py`: Client for interacting with Cerebras API

### Routes
- `routes/clean.py`: Data cleaning functionality
- `routes/generate.py`: Synthetic data generation functionality
- `routes/embed.py`: Data vectorization functionality
- `routes/enrich.py`: Data enrichment functionality
- `routes/download.py`: File download handlers

### Prompts
- `prompts/clean_template.txt`: Prompt template for data cleaning tasks
- `prompts/generate_template.txt`: Prompt template for data generation tasks
- `prompts/embed_template.txt`: Prompt template for data vectorization tasks
- `prompts/enrich_template.txt`: Prompt template for data enrichment tasks

## Data Flow

1. User interacts with frontend via natural language prompt
2. Frontend sends request to backend `/api/process` endpoint
3. Backend parses prompt to determine required actions
4. Backend routes process data using Cerebras API and other tools
5. Results are returned to frontend for display
6. User can download processed data using download buttons

## Key Features Implementation

### Dataset Cleaning
- Implemented in `backend/routes/clean.py`
- Uses `backend/prompts/clean_template.txt` for LLM instructions
- Basic preprocessing done before sending to LLM

### Fake Data Generation
- Implemented in `backend/routes/generate.py`
- Uses `backend/prompts/generate_template.txt` for LLM instructions
- Parses prompt to determine number and type of examples

### Vectorization for RAG
- Implemented in `backend/routes/embed.py`
- Uses sentence-transformers library for embedding generation
- Creates FAISS index for efficient similarity search

### Data Enrichment
- Implemented in `backend/routes/enrich.py`
- Uses web search APIs (Brave or Serper.dev) for enrichment
- Uses `backend/prompts/enrich_template.txt` for LLM instructions

### Download Handlers
- Implemented in `backend/routes/download.py`
- Provides endpoints for downloading data in various formats
- Supports CSV, JSON, and FAISS index downloads
