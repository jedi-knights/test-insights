"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getSuite, getSuiteMetrics } from "@/lib/api/suites";
import { getRuns } from "@/lib/api/runs";
import { MetricsCard } from "@/components/shared/metrics-card";
import { PassRateChart } from "@/components/charts/pass-rate-chart";
import { TestCountBar } from "@/components/charts/test-count-bar";
import { DurationTrendChart } from "@/components/charts/duration-trend-chart";
import { StatusBadge } from "@/components/shared/status-badge";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  params: { id: string };
}

export default function SuiteDetailPage({ params }: Props) {
  const { id } = params;
  const { data: suite, isLoading } = useQuery({
    queryKey: ["suite", id],
    queryFn: () => getSuite(id),
  });
  const { data: metrics } = useQuery({
    queryKey: ["suite-metrics", id],
    queryFn: () => getSuiteMetrics(id),
  });
  const { data: runs } = useQuery({
    queryKey: ["runs", id],
    queryFn: () => getRuns(id),
  });

  if (isLoading) return <LoadingSkeleton />;
  if (!suite) return <p>Suite not found.</p>;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">
          <Link href={`/projects/${suite.project_id}`} className="hover:underline">Project</Link> / Suite
        </p>
        <h1 className="text-2xl font-bold">{suite.name}</h1>
        {suite.description && <p className="text-muted-foreground">{suite.description}</p>}
      </div>

      {metrics && (
        <div className="grid gap-4 md:grid-cols-3">
          <MetricsCard title="Runs" value={metrics.total_runs} />
          <MetricsCard title="Pass Rate" value={`${Math.round(metrics.overall_pass_rate * 100)}%`} />
        </div>
      )}

      {metrics?.pass_rate_trend && metrics.pass_rate_trend.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Pass Rate Trend</CardTitle></CardHeader>
          <CardContent><PassRateChart data={metrics.pass_rate_trend} /></CardContent>
        </Card>
      )}

      {runs && runs.length > 0 && (
        <>
          <Card>
            <CardHeader><CardTitle>Test Counts per Run</CardTitle></CardHeader>
            <CardContent><TestCountBar runs={runs} /></CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle>Duration Trend</CardTitle></CardHeader>
            <CardContent><DurationTrendChart runs={runs} /></CardContent>
          </Card>
        </>
      )}

      <Card>
        <CardHeader><CardTitle>Test Runs</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2">
            {runs?.map((r) => (
              <div key={r.id} className="flex items-center justify-between rounded-md border p-3">
                <div>
                  <Link href={`/runs/${r.id}`} className="text-primary hover:underline font-medium font-mono text-sm">
                    {r.id.slice(0, 12)}…
                  </Link>
                  {r.branch && <span className="text-muted-foreground text-xs ml-2">{r.branch}</span>}
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-muted-foreground">
                    {r.passed_tests}/{r.total_tests} passed
                  </span>
                  <StatusBadge status={r.status} />
                </div>
              </div>
            ))}
            {runs?.length === 0 && <p className="text-muted-foreground">No runs yet.</p>}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
