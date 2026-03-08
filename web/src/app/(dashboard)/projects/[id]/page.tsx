"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getProject, getProjectMetrics } from "@/lib/api/projects";
import { getSuites } from "@/lib/api/suites";
import { MetricsCard } from "@/components/shared/metrics-card";
import { PassRateChart } from "@/components/charts/pass-rate-chart";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  params: Promise<{ id: string }>;
}

export default function ProjectDetailPage({ params }: Props) {
  const { id } = use(params);
  const { data: project, isLoading } = useQuery({
    queryKey: ["project", id],
    queryFn: () => getProject(id),
  });
  const { data: metrics } = useQuery({
    queryKey: ["project-metrics", id],
    queryFn: () => getProjectMetrics(id),
  });
  const { data: suites } = useQuery({
    queryKey: ["suites", id],
    queryFn: () => getSuites(id),
  });

  if (isLoading) return <LoadingSkeleton />;
  if (!project) return <p>Project not found.</p>;

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-muted-foreground">
          <Link href={`/teams/${project.team_id}`} className="hover:underline">Team</Link> / Project
        </p>
        <h1 className="text-2xl font-bold">{project.name}</h1>
        {project.description && <p className="text-muted-foreground">{project.description}</p>}
      </div>

      {metrics && (
        <div className="grid gap-4 md:grid-cols-3">
          <MetricsCard title="Suites" value={metrics.total_suites} />
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

      <Card>
        <CardHeader><CardTitle>Test Suites</CardTitle></CardHeader>
        <CardContent>
          {suites?.length === 0 ? (
            <p className="text-muted-foreground">No suites yet.</p>
          ) : (
            <ul className="space-y-2">
              {suites?.map((s) => (
                <li key={s.id}>
                  <Link href={`/suites/${s.id}`} className="text-primary hover:underline font-medium">
                    {s.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
