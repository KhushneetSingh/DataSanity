"""
Turso (libSQL) database utility.

Uses libsql_experimental to connect to a Turso cloud database.
Requires the following environment variables:
  - TURSO_DATABASE_URL   (e.g. libsql://your-db-name-your-org.turso.io)
  - TURSO_AUTH_TOKEN
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import libsql_experimental as libsql


_conn = None


def get_connection():
    """Return a cached database connection, creating it on first call."""
    global _conn
    if _conn is None:
        url = os.environ["TURSO_DATABASE_URL"]
        token = os.environ["TURSO_AUTH_TOKEN"]
        _conn = libsql.connect(database=url, auth_token=token)
    return _conn


def init_db():
    """Create the datasets table if it doesn't exist."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS datasets (
            id          TEXT PRIMARY KEY,
            filename    TEXT NOT NULL,
            r2_key      TEXT NOT NULL,
            rows        INTEGER DEFAULT 0,
            columns     INTEGER DEFAULT 0,
            size_bytes  INTEGER DEFAULT 0,
            health_score REAL DEFAULT NULL,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
        """
    )
    conn.commit()


def insert_dataset(
    filename: str,
    r2_key: str,
    rows: int = 0,
    columns: int = 0,
    size_bytes: int = 0,
) -> str:
    """Insert a new dataset record and return its ID."""
    conn = get_connection()
    dataset_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO datasets (id, filename, r2_key, rows, columns, size_bytes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (dataset_id, filename, r2_key, rows, columns, size_bytes, now, now),
    )
    conn.commit()
    return dataset_id


def update_health_score(dataset_id: str, score: float):
    """Update the health score for a dataset."""
    conn = get_connection()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "UPDATE datasets SET health_score = ?, updated_at = ? WHERE id = ?",
        (score, now, dataset_id),
    )
    conn.commit()


def get_dataset(dataset_id: str) -> Optional[dict]:
    """Fetch a single dataset by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM datasets WHERE id = ?", (dataset_id,)).fetchone()
    if row is None:
        return None
    columns = ["id", "filename", "r2_key", "rows", "columns", "size_bytes", "health_score", "created_at", "updated_at"]
    return dict(zip(columns, row))


def list_datasets() -> list[dict]:
    """Fetch all datasets ordered by creation date descending."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM datasets ORDER BY created_at DESC").fetchall()
    columns = ["id", "filename", "r2_key", "rows", "columns", "size_bytes", "health_score", "created_at", "updated_at"]
    return [dict(zip(columns, row)) for row in rows]


def delete_dataset(dataset_id: str):
    """Delete a dataset record by ID."""
    conn = get_connection()
    conn.execute("DELETE FROM datasets WHERE id = ?", (dataset_id,))
    conn.commit()
