# DataSanity Setup Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- pip (Python package manager)
- npm (Node package manager)

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:
   ```env
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   EXA_API_KEY=your_exa_api_key_here  # Optional, for web search enrichment
   SERPER_API_KEY=your_serper_api_key_here  # Optional, for web search enrichment
   ```

5. Run the backend server:
   ```bash
   python main.py
   ```
   The backend will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Run the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

## Using the Application

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a data processing prompt in the text area, such as:
   - "Clean this dataset and generate 30 new noisy examples"
   - "Vectorize the text columns in my dataset"
   - "Enrich the ambiguous fields in my data"
3. Optionally upload a CSV file
4. Click "Process Data" to send the request to the backend
5. View the results in the tables displayed
6. Use the download buttons to save processed data in various formats

## API Endpoints

- `POST /api/process` - Main processing endpoint that handles all data operations
- `GET /api/download/csv` - Download processed data as CSV
- `GET /api/download/json` - Download processed data as JSON
- `GET /api/download/faiss` - Download FAISS vector index

## Features

- **Dataset Cleaning**: Detects and removes noisy, missing, or duplicate values using LLM intelligence
- **Fake Data Generation**: Generates synthetic data based on schema or prompt with or without noise
- **Vectorization**: Converts text-based records into embeddings suitable for RAG pipelines
- **Data Enrichment**: Enriches ambiguous fields with relevant context from web search APIs
- **Natural Language Interface**: Users interact using natural language to describe what they want

## Tech Stack

- **Frontend**: Next.js with Tailwind CSS
- **Backend**: FastAPI in Python
- **LLM Inference**: Cerebras API (Code LLaMA 13B or LLaMA 2 13B Instruct)
- **Data Tools**: pandas, numpy, pyarrow
- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Web Search API**: Exa or Serper.dev
- **Storage**: SQLite for temp + local filesystem (CSV/JSON/FAISS)
