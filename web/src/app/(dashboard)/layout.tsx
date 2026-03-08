"use client";

import { useRequireAuth } from "@/lib/auth/hooks";
import { Sidebar } from "@/components/layout/sidebar";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { loading } = useRequireAuth();

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <LoadingSkeleton />
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-auto p-6">{children}</main>
    </div>
  );
}
