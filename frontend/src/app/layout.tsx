import type { Metadata } from "next"
import "./globals.css"
import { Toaster } from "@/components/ui/sonner"

export const metadata: Metadata = {
  title: "DataSanity — Data Operations",
  description: "Monitor your data health and run AI-powered operations",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0a0a0a] text-[#f0f0f0] antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  )
}
