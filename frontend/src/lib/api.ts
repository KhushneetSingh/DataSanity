const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export async function uploadDataset(file: File): Promise<{ dataset_id: string }> {
  const form = new FormData()
  form.append("file", file)
  const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form })
  if (!res.ok) throw new Error("Upload failed")
  return res.json()
}

export async function getDatasets() {
  const res = await fetch(`${API_BASE}/datasets`)
  if (!res.ok) throw new Error("Failed to fetch datasets")
  return res.json()
}
