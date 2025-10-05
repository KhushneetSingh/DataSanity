import pandas as pd
from fastapi import APIRouter, Response
from fastapi.responses import FileResponse
import io
import os
import faiss
import json

router = APIRouter()

@router.get("/api/download/csv")
async def download_csv():
    """
    Download processed data as CSV file.
    """
    # In a real implementation, this would retrieve the processed data
    # For this MVP, we'll create a sample CSV
    
    # Create sample data
    data = {
        "Name": ["John Doe", "Jane Smith", "Bob Johnson"],
        "Age": [29, 34, 41],
        "City": ["New York", "London", "Paris"],
        "Occupation": ["Engineer", "Doctor", "Teacher"]
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=processed_data.csv"}
    )

@router.get("/api/download/json")
async def download_json():
    """
    Download processed data as JSON file.
    """
    # In a real implementation, this would retrieve the processed data
    # For this MVP, we'll create a sample JSON
    
    # Create sample data
    data = {
        "dataset_info": {
            "rows": 3,
            "columns": 4,
            "processing_date": "2025-04-10"
        },
        "data": [
            {"Name": "John Doe", "Age": 29, "City": "New York", "Occupation": "Engineer"},
            {"Name": "Jane Smith", "Age": 34, "City": "London", "Occupation": "Doctor"},
            {"Name": "Bob Johnson", "Age": 41, "City": "Paris", "Occupation": "Teacher"}
        ]
    }
    
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=processed_data.json"}
    )

@router.get("/api/download/faiss")
async def download_faiss():
    """
    Download FAISS index file.
    """
    # Check if FAISS index file exists
    faiss_file_path = "faiss_index.bin"
    if not os.path.exists(faiss_file_path):
        return {"error": "FAISS index file not found"}
    
    return FileResponse(
        path=faiss_file_path,
        media_type="application/octet-stream",
        filename="faiss_index.bin"
    )
