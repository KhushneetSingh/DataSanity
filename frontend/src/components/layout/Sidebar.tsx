"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Home, Database, GitBranch, History, Settings, Plus, Zap
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

const navItems = [
  { href: "/", label: "Home", icon: Home },
  { href: "/datasets", label: "Datasets", icon: Database },
  { href: "/pipelines", label: "Pipelines", icon: GitBranch },
  { href: "/history", label: "History", icon: History },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="flex flex-col w-[220px] min-h-screen bg-[#0d0d0d] border-r border-[#1f1f1f] fixed left-0 top-0 bottom-0 z-40">
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-4 py-4 border-b border-[#1f1f1f]">
        <div className="w-7 h-7 rounded-md bg-[#7c3aed] flex items-center justify-center">
          <Zap className="w-4 h-4 text-white" />
        </div>
        <div>
          <p className="text-sm font-semibold text-[#f0f0f0] leading-none">DataSanity</p>
          <p className="text-[10px] text-[#555] mt-0.5">Data Operations</p>
        </div>
      </div>

      {/* New Project Button */}
      <div className="px-3 py-3">
        <Button
          className="w-full bg-[#7c3aed] hover:bg-[#6d28d9] text-white text-sm h-8 rounded-md font-medium"
          size="sm"
        >
          <Plus className="w-3.5 h-3.5 mr-1.5" />
          New Project
        </Button>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-2 py-1 space-y-0.5">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href || (href !== "/" && pathname.startsWith(href))
          return (
            <Link key={href} href={href}>
              <div className={cn(
                "flex items-center gap-2.5 px-3 py-2 rounded-md text-sm cursor-pointer transition-colors",
                active
                  ? "bg-[#1a1a1a] text-[#f0f0f0]"
                  : "text-[#8a8a8a] hover:text-[#f0f0f0] hover:bg-[#151515]"
              )}>
                <Icon className="w-4 h-4 flex-shrink-0" />
                {label}
              </div>
            </Link>
          )
        })}
      </nav>

      {/* User footer */}
      <div className="px-3 py-3 border-t border-[#1f1f1f]">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-[#1f1f1f] border border-[#2a2a2a] flex items-center justify-center text-xs text-[#8a8a8a]">
            A
          </div>
          <div>
            <p className="text-xs font-medium text-[#f0f0f0] leading-none">Admin User</p>
            <p className="text-[10px] text-[#555] mt-0.5">admin@datasanity.io</p>
          </div>
        </div>
      </div>
    </aside>
  )
}
