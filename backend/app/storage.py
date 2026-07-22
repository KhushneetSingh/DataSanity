import boto3
from botocore.config import Config
from app.config import settings

def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key,
        aws_secret_access_key=settings.r2_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

def upload_to_r2(file_bytes: bytes, r2_key: str, content_type: str = "application/octet-stream") -> str:
    """Upload bytes to R2 and return the key."""
    client = get_r2_client()
    client.put_object(
        Bucket=settings.r2_bucket_name,
        Key=r2_key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return r2_key

def download_from_r2(r2_key: str) -> bytes:
    """Download file bytes from R2."""
    client = get_r2_client()
    response = client.get_object(Bucket=settings.r2_bucket_name, Key=r2_key)
    return response["Body"].read()

def get_presigned_url(r2_key: str, expires_in: int = 3600) -> str:
    """Generate a presigned download URL."""
    client = get_r2_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.r2_bucket_name, "Key": r2_key},
        ExpiresIn=expires_in,
    )
