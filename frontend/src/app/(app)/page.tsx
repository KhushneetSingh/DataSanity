"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useDropzone } from "react-dropzone"
import { Database, Table2, Braces, Clock, CheckCircle, AlertCircle, CloudUpload, Plus } from "lucide-react"
import { Topbar } from "@/components/layout/Topbar"
import { HealthBadge } from "@/components/ui/HealthBadge"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { toast } from "sonner"

// --- Mock data (will be replaced with Supabase in Phase 2) ---
const recentDatasets = [
  {
    id: "1", name: "customer_orders_2024.csv", icon: Table2,
    rows: "1.2M rows", modified: "10 mins ago", score: 82,
  },
  {
    id: "2", name: "user_events_raw.db", icon: Database,
    rows: "8.4M rows", modified: "2 hrs ago", score: 64,
  },
  {
    id: "3", name: "product_catalog_v2.json", icon: Braces,
    rows: "45K items", modified: "Yesterday", score: 98,
  },
]

const recentOps = [
  { id: "1", label: "Cleaned", file: "orders.csv", time: "2 min ago", status: "success" },
  { id: "2", label: "Enriched", file: "leads.db", time: "1 hour ago", status: "success" },
  { id: "3", label: "Schema updated for", file: "users_v2", time: "3 hours ago", status: "warning" },
  { id: "4", label: "Failed pipeline", file: "sync_crm", time: "Yesterday", status: "error" },
]

export default function DashboardPage() {
  const router = useRouter()
  const [uploading, setUploading] = useState(false)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "text/csv": [".csv"],
      "application/json": [".json"],
      "application/octet-stream": [".db"],
    },
    onDrop: async (files) => {
      if (!files[0]) return
      setUploading(true)
      try {
        const form = new FormData()
        form.append("file", files[0])
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, {
          method: "POST",
          body: form,
        })
        const data = await res.json()
        if (!res.ok) throw new Error(data.detail || "Upload failed")
        toast.success("Upload successful", { description: `${files[0].name} is ready to explore.` })
        router.push(`/datasets/${data.dataset_id}`)
      } catch (e: unknown) {
        const message = e instanceof Error ? e.message : "Upload failed"
        toast.error("Upload failed", { description: message })
      } finally {
        setUploading(false)
      }
    },
  })

  return (
    <div className="flex flex-col min-h-screen">
      <Topbar
        action={
          <Button className="bg-[#7c3aed] hover:bg-[#6d28d9] text-white h-8 text-xs rounded-md px-3">
            <Plus className="w-3.5 h-3.5 mr-1.5" />
            New Dataset
          </Button>
        }
      />

      <div className="px-8 py-6 flex-1">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-semibold text-[#f0f0f0]">Dashboard Overview</h1>
          <p className="text-sm text-[#8a8a8a] mt-1">Monitor your data health and recent activities.</p>
        </div>

        {/* Recent Datasets */}
        <section className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-medium text-[#f0f0f0]">Recent Datasets</h2>
            <button className="text-xs text-[#7c3aed] hover:underline">View all</button>
          </div>
          <div className="grid grid-cols-3 gap-3">
            {recentDatasets.map((ds) => {
              const Icon = ds.icon
              return (
                <button
                  key={ds.id}
                  onClick={() => router.push(`/datasets/${ds.id}`)}
                  className="flex flex-col bg-[#111] border border-[#1f1f1f] rounded-lg p-4 text-left hover:border-[#2a2a2a] hover:bg-[#141414] transition-all group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Icon className="w-4 h-4 text-[#555]" />
                      <span className="text-xs font-mono text-[#f0f0f0] truncate max-w-[130px]">{ds.name}</span>
                    </div>
                    <HealthBadge score={ds.score} />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <p className="text-[9px] uppercase tracking-wider text-[#555] mb-1">Rows</p>
                      <p className="text-xs font-medium text-[#f0f0f0]">{ds.rows}</p>
                    </div>
                    <div>
                      <p className="text-[9px] uppercase tracking-wider text-[#555] mb-1">Modified</p>
                      <p className="text-xs text-[#8a8a8a]">{ds.modified}</p>
                    </div>
                  </div>
                </button>
              )
            })}
          </div>
        </section>

        {/* Bottom row */}
        <div className="grid grid-cols-2 gap-4">
          {/* Recent Operations */}
          <div className="bg-[#111] border border-[#1f1f1f] rounded-lg p-4">
            <h2 className="text-sm font-medium text-[#f0f0f0] mb-4">Recent Operations</h2>
            <div className="space-y-3">
              {recentOps.map((op) => (
                <div key={op.id} className="flex items-center gap-3">
                  <div className={cn("w-6 h-6 rounded-md flex items-center justify-center flex-shrink-0", {
                    "bg-[#22c55e15]": op.status === "success",
                    "bg-[#f59e0b15]": op.status === "warning",
                    "bg-[#ef444415]": op.status === "error",
                  })}>
                    {op.status === "success" && <CheckCircle className="w-3.5 h-3.5 text-[#22c55e]" />}
                    {op.status === "warning" && <Clock className="w-3.5 h-3.5 text-[#f59e0b]" />}
                    {op.status === "error" && <AlertCircle className="w-3.5 h-3.5 text-[#ef4444]" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-[#f0f0f0] truncate">
                      {op.label} <code className="font-mono text-[#7c3aed]">{op.file}</code>
                    </p>
                    <p className="text-[10px] text-[#555]">{op.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Upload Zone */}
          <div
            {...getRootProps()}
            className={cn(
              "bg-[#0d0d0d] border-2 border-dashed border-[#1f1f1f] rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer transition-all",
              isDragActive && "border-[#7c3aed] bg-[#7c3aed08]",
              uploading && "opacity-60 pointer-events-none"
            )}
          >
            <input {...getInputProps()} />
            <div className="w-12 h-12 rounded-xl bg-[#7c3aed15] flex items-center justify-center mb-3">
              <CloudUpload className="w-6 h-6 text-[#7c3aed]" />
            </div>
            <p className="text-sm font-medium text-[#f0f0f0] mb-1">
              {uploading ? "Uploading..." : "Upload new dataset"}
            </p>
            <p className="text-xs text-[#555] text-center mb-3">
              Drag and drop your CSV, JSON, or DB files here, or click to browse.
            </p>
            <div className="flex gap-2">
              {[".csv", ".json", ".db"].map((ext) => (
                <span key={ext} className="text-[10px] font-mono text-[#8a8a8a] bg-[#1a1a1a] border border-[#2a2a2a] rounded px-2 py-0.5">
                  {ext}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
