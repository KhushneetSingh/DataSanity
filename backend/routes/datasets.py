"""
Datasets listing and management endpoints.
"""

from fastapi import APIRouter, HTTPException
from utils.database import list_datasets, get_dataset, delete_dataset
from utils.storage import delete_file as r2_delete, generate_presigned_url

router = APIRouter()


@router.get("/api/datasets")
async def get_datasets():
    """Return all datasets sorted by creation date (newest first)."""
    datasets = list_datasets()
    return {"datasets": datasets}


@router.get("/api/datasets/{dataset_id}")
async def get_single_dataset(dataset_id: str):
    """Return a single dataset by ID."""
    dataset = get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.get("/api/datasets/{dataset_id}/download-url")
async def get_download_url(dataset_id: str):
    """Generate a presigned download URL for a dataset's file."""
    dataset = get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    url = generate_presigned_url(dataset["r2_key"], expires_in=3600)
    return {"url": url}


@router.delete("/api/datasets/{dataset_id}")
async def remove_dataset(dataset_id: str):
    """Delete a dataset record and its file from R2."""
    dataset = get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    # Remove from R2
    try:
        r2_delete(dataset["r2_key"])
    except Exception:
        pass  # Best-effort deletion
    # Remove from DB
    delete_dataset(dataset_id)
    return {"status": "deleted", "id": dataset_id}
