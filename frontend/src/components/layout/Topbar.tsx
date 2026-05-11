import { Search, Bell, HelpCircle } from "lucide-react"
import { Button } from "@/components/ui/button"

interface TopbarProps {
  title?: string
  action?: React.ReactNode
}

export function Topbar({ action }: TopbarProps) {
  return (
    <header className="flex items-center justify-between px-6 h-12 border-b border-[#1f1f1f] sticky top-0 bg-[#0a0a0a] z-30">
      <div className="flex-1" />
      <div className="flex items-center gap-2">
        {/* Search */}
        <div className="flex items-center gap-2 bg-[#111] border border-[#1f1f1f] rounded-md px-3 h-8 text-sm text-[#555] w-52">
          <Search className="w-3.5 h-3.5 text-[#555]" />
          <span>Search resources...</span>
        </div>
        <Button variant="ghost" size="icon" className="w-8 h-8 text-[#555] hover:text-[#f0f0f0]">
          <Bell className="w-4 h-4" />
        </Button>
        <Button variant="ghost" size="icon" className="w-8 h-8 text-[#555] hover:text-[#f0f0f0]">
          <HelpCircle className="w-4 h-4" />
        </Button>
        {action && action}
      </div>
    </header>
  )
}
