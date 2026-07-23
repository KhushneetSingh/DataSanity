import os
import boto3
from botocore.config import Config
from app.config import settings
from pathlib import Path

# Setup local storage directory
LOCAL_STORAGE_DIR = Path("uploads")
USE_LOCAL = os.getenv("USE_LOCAL_STORAGE", "true").lower() == "true"

if USE_LOCAL:
    LOCAL_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def get_r2_client():
    if USE_LOCAL:
        return None
        
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key,
        aws_secret_access_key=settings.r2_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

def upload_to_r2(file_bytes: bytes, r2_key: str, content_type: str = "application/octet-stream") -> str:
    """Upload bytes to R2 (or local storage) and return the key."""
    if USE_LOCAL:
        local_path = LOCAL_STORAGE_DIR / r2_key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with open(local_path, "wb") as f:
            f.write(file_bytes)
        return r2_key

    client = get_r2_client()
    client.put_object(
        Bucket=settings.r2_bucket_name,
        Key=r2_key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return r2_key

def download_from_r2(r2_key: str) -> bytes:
    """Download file bytes from R2 (or local storage)."""
    if USE_LOCAL:
        local_path = LOCAL_STORAGE_DIR / r2_key
        with open(local_path, "rb") as f:
            return f.read()

    client = get_r2_client()
    response = client.get_object(Bucket=settings.r2_bucket_name, Key=r2_key)
    return response["Body"].read()

def get_presigned_url(r2_key: str, expires_in: int = 3600) -> str:
    """Generate a presigned download URL."""
    if USE_LOCAL:
        # For local dev, we could just return a mock URL, 
        # but returning the key is often enough if the frontend uses a local proxy
        return f"http://localhost:8000/static/{r2_key}"

    client = get_r2_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.r2_bucket_name, "Key": r2_key},
        ExpiresIn=expires_in,
    )
