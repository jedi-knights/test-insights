"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getRun } from "@/lib/api/runs";
import { MetricsCard } from "@/components/shared/metrics-card";
import { StatusBadge } from "@/components/shared/status-badge";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  params: { id: string };
}

export default function RunDetailPage({ params }: Props) {
  const { id } = params;
  const { data, isLoading } = useQuery({
    queryKey: ["run", id],
    queryFn: () => getRun(id),
  });

  if (isLoading) return <LoadingSkeleton />;
  if (!data) return <p>Run not found.</p>;

  const { run, cases } = data;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">
          <Link href={`/suites/${run.suite_id}`} className="hover:underline">Suite</Link> / Run
        </p>
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold font-mono">{run.id.slice(0, 16)}…</h1>
          <StatusBadge status={run.status} />
        </div>
        <div className="flex gap-4 text-sm text-muted-foreground mt-1">
          {run.branch && <span>Branch: <strong>{run.branch}</strong></span>}
          {run.commit_sha && <span>Commit: <code className="text-xs">{run.commit_sha.slice(0, 8)}</code></span>}
          <span>Build: {run.build_system}</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <MetricsCard title="Total" value={run.total_tests} />
        <MetricsCard title="Passed" value={run.passed_tests} />
        <MetricsCard title="Failed" value={run.failed_tests} />
        <MetricsCard title="Skipped" value={run.skipped_tests} />
      </div>

      <Card>
        <CardHeader><CardTitle>Test Cases ({cases.length})</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2">
            {cases.map((c) => (
              <div key={c.id} className="rounded-md border p-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-sm truncate">{c.name}</p>
                    {c.classname && <p className="text-xs text-muted-foreground">{c.classname}</p>}
                    {c.error_message && (
                      <pre className="mt-2 text-xs bg-destructive/10 text-destructive rounded p-2 overflow-auto max-h-24">
                        {c.error_message}
                      </pre>
                    )}
                  </div>
                  <div className="ml-3 flex-shrink-0">
                    <StatusBadge status={c.status} />
                  </div>
                </div>
              </div>
            ))}
            {cases.length === 0 && <p className="text-muted-foreground">No test cases recorded.</p>}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
