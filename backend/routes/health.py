"""
Health score computation endpoint.

Computes a data-quality score (0–100) based on:
  - Completeness  (% of non-null cells)
  - Uniqueness    (% of non-duplicate rows)
  - Consistency   (basic type-consistency check per column)
"""

import io
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from utils.database import get_dataset, update_health_score
from utils.storage import download_file

router = APIRouter()


class HealthScoreResponse(BaseModel):
    dataset_id: str
    overall_score: float
    completeness: float
    uniqueness: float
    consistency: float
    total_rows: int
    total_columns: int
    missing_cells: int
    duplicate_rows: int


def _compute_health(df: pd.DataFrame) -> dict:
    """Compute health metrics for a DataFrame."""
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = int(df.isnull().sum().sum())
    completeness = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 100.0

    duplicate_rows = int(df.duplicated().sum())
    uniqueness = ((df.shape[0] - duplicate_rows) / df.shape[0] * 100) if df.shape[0] > 0 else 100.0

    # Consistency: for each column, check if the non-null values are all the same inferred type
    consistent_cols = 0
    for col in df.columns:
        non_null = df[col].dropna()
        if len(non_null) == 0:
            consistent_cols += 1
            continue
        # Try numeric conversion
        numeric = pd.to_numeric(non_null, errors="coerce")
        numeric_ratio = numeric.notna().sum() / len(non_null)
        # If ≥90% parse as numbers OR ≤10% parse as numbers → consider consistent
        if numeric_ratio >= 0.9 or numeric_ratio <= 0.1:
            consistent_cols += 1
    consistency = (consistent_cols / len(df.columns) * 100) if len(df.columns) > 0 else 100.0

    overall = round(completeness * 0.4 + uniqueness * 0.35 + consistency * 0.25, 2)

    return {
        "overall_score": overall,
        "completeness": round(completeness, 2),
        "uniqueness": round(uniqueness, 2),
        "consistency": round(consistency, 2),
        "total_rows": df.shape[0],
        "total_columns": df.shape[1],
        "missing_cells": missing_cells,
        "duplicate_rows": duplicate_rows,
    }


@router.get("/api/health-score/{dataset_id}", response_model=HealthScoreResponse)
async def get_health_score(dataset_id: str):
    """Compute and return the health score for a stored dataset."""
    dataset = get_dataset(dataset_id)
    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Download CSV from R2
    try:
        file_bytes = download_file(dataset["r2_key"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download dataset from storage: {e}")

    df = pd.read_csv(io.BytesIO(file_bytes))
    metrics = _compute_health(df)

    # Persist the overall score
    update_health_score(dataset_id, metrics["overall_score"])

    return HealthScoreResponse(dataset_id=dataset_id, **metrics)
