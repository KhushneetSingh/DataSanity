import uuid
import io
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd

from app.database import get_supabase
from app.storage import upload_to_r2

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_EXTENSIONS = {".csv", ".json", ".db", ".parquet"}
MAX_FILE_SIZE_MB = 200

CONTENT_TYPE_MAP = {
    ".csv": "text/csv",
    ".json": "application/json",
    ".db": "application/octet-stream",
    ".parquet": "application/octet-stream",
}

@router.post("")
async def upload_dataset(file: UploadFile = File(...)):
    # Validate extension
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type {suffix} not supported. Use: {', '.join(ALLOWED_EXTENSIONS)}")

    # Read file
    file_bytes = await file.read()
    file_size = len(file_bytes)

    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large. Max {MAX_FILE_SIZE_MB}MB.")

    # Detect row/column count
    row_count = None
    col_count = None
    try:
        if suffix == ".csv":
            df = pd.read_csv(io.BytesIO(file_bytes), nrows=5000)
            # Get total rows without loading all data
            total_df = pd.read_csv(io.BytesIO(file_bytes), usecols=[0])
            row_count = len(total_df)
            col_count = len(df.columns)
        elif suffix == ".json":
            df = pd.read_json(io.BytesIO(file_bytes))
            row_count = len(df)
            col_count = len(df.columns)
        elif suffix == ".parquet":
            df = pd.read_parquet(io.BytesIO(file_bytes))
            row_count = len(df)
            col_count = len(df.columns)
    except Exception:
        pass  # Non-critical; proceed with nulls

    # Upload to R2
    dataset_id = str(uuid.uuid4())
    r2_key = f"datasets/{dataset_id}/original{suffix}"
    upload_to_r2(file_bytes, r2_key, CONTENT_TYPE_MAP.get(suffix, "application/octet-stream"))

    # Insert into Supabase
    db = get_supabase()
    result = db.table("datasets").insert({
        "id": dataset_id,
        "name": file.filename,
        "original_filename": file.filename,
        "file_type": suffix.lstrip("."),
        "r2_key": r2_key,
        "row_count": row_count,
        "column_count": col_count,
        "file_size_bytes": file_size,
        "status": "ready",
    }).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save dataset metadata")

    return JSONResponse({"dataset_id": dataset_id, "name": file.filename, "row_count": row_count})


@router.get("/datasets")
async def list_datasets():
    db = get_supabase()
    result = db.table("datasets").select("*").order("created_at", desc=True).limit(20).execute()
    return result.data
