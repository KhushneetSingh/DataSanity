"""
Cloudflare R2 storage utility.

Uses boto3 with S3-compatible API to interact with Cloudflare R2.
Requires the following environment variables:
  - R2_ACCESS_KEY_ID
  - R2_SECRET_ACCESS_KEY
  - R2_ENDPOINT_URL        (e.g. https://<account-id>.r2.cloudflarestorage.com)
  - R2_BUCKET_NAME          (e.g. datasanity)
"""

import os
import io
import boto3
from botocore.config import Config


def _get_client():
    """Create and return a boto3 S3 client configured for Cloudflare R2."""
    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT_URL"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def _bucket():
    return os.environ.get("R2_BUCKET_NAME", "datasanity")


def upload_file(file_bytes: bytes, key: str, content_type: str = "text/csv") -> str:
    """
    Upload a file to R2 and return the object key.

    Parameters
    ----------
    file_bytes : bytes
        Raw file content.
    key : str
        Object key / path inside the bucket (e.g. "datasets/abc123.csv").
    content_type : str
        MIME type of the file.

    Returns
    -------
    str
        The key that was written.
    """
    client = _get_client()
    client.put_object(
        Bucket=_bucket(),
        Key=key,
        Body=file_bytes,
        ContentType=content_type,
    )
    return key


def download_file(key: str) -> bytes:
    """Download a file from R2 and return raw bytes."""
    client = _get_client()
    response = client.get_object(Bucket=_bucket(), Key=key)
    return response["Body"].read()


def generate_presigned_url(key: str, expires_in: int = 3600) -> str:
    """Generate a presigned download URL (valid for `expires_in` seconds)."""
    client = _get_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": _bucket(), "Key": key},
        ExpiresIn=expires_in,
    )


def delete_file(key: str) -> None:
    """Delete a file from R2."""
    client = _get_client()
    client.delete_object(Bucket=_bucket(), Key=key)


def list_files(prefix: str = "") -> list[dict]:
    """List objects in the bucket under a given prefix."""
    client = _get_client()
    response = client.list_objects_v2(Bucket=_bucket(), Prefix=prefix)
    return [
        {"key": obj["Key"], "size": obj["Size"], "last_modified": obj["LastModified"].isoformat()}
        for obj in response.get("Contents", [])
    ]
