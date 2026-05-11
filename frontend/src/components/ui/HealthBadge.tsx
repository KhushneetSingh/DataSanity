import { cn } from "@/lib/utils"

interface HealthBadgeProps {
  score: number
  className?: string
}

export function HealthBadge({ score, className }: HealthBadgeProps) {
  const color =
    score >= 85 ? "bg-[#22c55e20] text-[#22c55e] border-[#22c55e30]" :
    score >= 65 ? "bg-[#f59e0b20] text-[#f59e0b] border-[#f59e0b30]" :
                  "bg-[#ef444420] text-[#ef4444] border-[#ef444430]"

  return (
    <div className={cn(
      "inline-flex items-center justify-center w-10 h-10 rounded-full border text-xs font-semibold",
      color,
      className
    )}>
      {score}%
    </div>
  )
}
