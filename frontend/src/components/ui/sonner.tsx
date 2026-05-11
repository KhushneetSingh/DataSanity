"use client"

import { Toaster as Sonner, type ToasterProps } from "sonner"

const Toaster = ({ ...props }: ToasterProps) => {
  return (
    <Sonner
      theme="dark"
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-[#111] group-[.toaster]:text-[#f0f0f0] group-[.toaster]:border-[#1f1f1f] group-[.toaster]:shadow-lg",
          description: "group-[.toast]:text-[#8a8a8a]",
          actionButton:
            "group-[.toast]:bg-[#7c3aed] group-[.toast]:text-white",
          cancelButton:
            "group-[.toast]:bg-[#1f1f1f] group-[.toast]:text-[#8a8a8a]",
        },
      }}
      {...props}
    />
  )
}

export { Toaster }
