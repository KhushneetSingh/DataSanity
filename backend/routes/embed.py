import pandas as pd
from typing import Optional
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json
import os
from cerebras_client import cerebras_client

def vectorize_data(df: Optional[pd.DataFrame], prompt: str) -> str:
    """
    Convert text-based records into embeddings suitable for use in retrieval-augmented generation pipelines.
    Uses sentence-transformers and FAISS to create vector embeddings.
    """
    if df is None:
        return "No data provided for vectorization"
    
    # Get text columns (simplified approach)
    text_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    if not text_columns:
        return "No text columns found in the dataset for vectorization"
    
    # Load sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Combine text from all text columns for each row
    df['combined_text'] = df[text_columns].apply(
        lambda row: ' '.join([str(val) for val in row if pd.notna(val)]), axis=1
    )
    
    # Convert text data to embeddings
    texts = df['combined_text'].tolist()
    embeddings = model.encode(texts)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save FAISS index to disk
    faiss.write_index(index, "faiss_index.bin")
    
    # Save metadata for the embeddings
    metadata = []
    for i, text in enumerate(texts):
        metadata.append({
            "id": i,
            "text": text,
            "source_row": df.iloc[i].to_dict()
        })
    
    with open("embedding_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    # Load the embedding prompt template
    template_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "embed_template.txt")
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        return "Error: Embed template not found"
    
    # Fill the template with dataset and prompt
    filled_prompt = template.replace("{{dataset}}", df.head(5).to_csv(index=False))
    filled_prompt = filled_prompt.replace("{{prompt}}", prompt)
    
    # Call Cerebras API for intelligent vectorization
    api_response = cerebras_client.generate(filled_prompt, max_tokens=512)
    
    result = f"Data vectorization completed:\n"
    result += f"- Dataset shape: {df.shape}\n"
    result += f"- Text columns identified: {text_columns}\n"
    result += f"- Embedding model: sentence-transformers/all-MiniLM-L6-v2\n"
    result += f"- Vector dimension: {dimension}\n"
    result += f"- FAISS index created: True\n"
    result += f"- FAISS index saved to: faiss_index.bin\n"
    result += f"- Metadata saved to: embedding_metadata.json\n\n"
    
    if api_response["success"]:
        result += f"Vectorization summary from Cerebras API:\n{api_response['response']}\n\n"
    else:
        result += f"Note: Cerebras API call failed, using default vectorization\n"
        result += f"Error: {api_response['error']}\n\n"
    
    # Show sample embeddings
    result += "Sample embeddings (first 3 rows):\n"
    for i in range(min(3, len(embeddings))):
        # Show first 5 dimensions of the embedding vector
        sample_vector = embeddings[i][:5]
        result += f"Row {i+1}: [{', '.join([f'{val:.2f}' for val in sample_vector])}, ...]\n"
    
    return result
