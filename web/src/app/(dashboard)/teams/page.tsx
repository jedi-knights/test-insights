"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { getTeams } from "@/lib/api/teams";
import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function TeamsPage() {
  const { data: teams, isLoading } = useQuery({ queryKey: ["teams"], queryFn: getTeams });

  if (isLoading) return <LoadingSkeleton />;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Teams</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {teams?.map((team) => (
          <Link key={team.id} href={`/teams/${team.id}`}>
            <Card className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle className="text-base">{team.name}</CardTitle>
              </CardHeader>
              {team.description && (
                <CardContent>
                  <p className="text-sm text-muted-foreground">{team.description}</p>
                </CardContent>
              )}
            </Card>
          </Link>
        ))}
        {teams?.length === 0 && (
          <p className="text-muted-foreground col-span-3">No teams yet.</p>
        )}
      </div>
    </div>
  );
}
