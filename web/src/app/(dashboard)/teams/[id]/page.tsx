"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getTeam, getTeamMetrics } from "@/lib/api/teams";
import { getProjects } from "@/lib/api/projects";
import { MetricsCard } from "@/components/shared/metrics-card";
import { PassRateChart } from "@/components/charts/pass-rate-chart";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Props {
  params: Promise<{ id: string }>;
}

export default function TeamDetailPage({ params }: Props) {
  const { id } = use(params);
  const { data: team, isLoading: teamLoading } = useQuery({
    queryKey: ["team", id],
    queryFn: () => getTeam(id),
  });
  const { data: metrics } = useQuery({
    queryKey: ["team-metrics", id],
    queryFn: () => getTeamMetrics(id),
  });
  const { data: projects } = useQuery({
    queryKey: ["projects", id],
    queryFn: () => getProjects(id),
  });

  if (teamLoading) return <LoadingSkeleton />;
  if (!team) return <p>Team not found.</p>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">{team.name}</h1>
        {team.description && <p className="text-muted-foreground">{team.description}</p>}
      </div>

      {metrics && (
        <div className="grid gap-4 md:grid-cols-4">
          <MetricsCard title="Projects" value={metrics.total_projects} />
          <MetricsCard title="Suites" value={metrics.total_suites} />
          <MetricsCard title="Runs" value={metrics.total_runs} />
          <MetricsCard
            title="Pass Rate"
            value={`${Math.round(metrics.overall_pass_rate * 100)}%`}
          />
        </div>
      )}

      {metrics?.pass_rate_trend && metrics.pass_rate_trend.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Pass Rate Trend</CardTitle></CardHeader>
          <CardContent>
            <PassRateChart data={metrics.pass_rate_trend} />
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader><CardTitle>Projects</CardTitle></CardHeader>
        <CardContent>
          {projects?.length === 0 ? (
            <p className="text-muted-foreground">No projects yet.</p>
          ) : (
            <ul className="space-y-2">
              {projects?.map((p) => (
                <li key={p.id}>
                  <Link href={`/projects/${p.id}`} className="text-primary hover:underline font-medium">
                    {p.name}
                  </Link>
                  {p.description && <span className="text-muted-foreground text-sm ml-2">— {p.description}</span>}
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
