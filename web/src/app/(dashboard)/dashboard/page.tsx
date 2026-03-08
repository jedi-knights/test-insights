"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getTeams } from "@/lib/api/teams";
import { MetricsCard } from "@/components/shared/metrics-card";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function DashboardPage() {
  const { data: teams, isLoading } = useQuery({ queryKey: ["teams"], queryFn: getTeams });

  if (isLoading) return <LoadingSkeleton />;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricsCard title="Total Teams" value={teams?.length ?? 0} />
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Teams</CardTitle>
        </CardHeader>
        <CardContent>
          {teams?.length === 0 ? (
            <p className="text-muted-foreground">No teams yet.</p>
          ) : (
            <ul className="space-y-2">
              {teams?.map((t) => (
                <li key={t.id}>
                  <Link href={`/teams/${t.id}`} className="text-primary hover:underline font-medium">
                    {t.name}
                  </Link>
                  {t.description && <span className="text-muted-foreground text-sm ml-2">— {t.description}</span>}
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
