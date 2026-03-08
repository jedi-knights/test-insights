"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TestRun } from "@/types";

interface DurationTrendChartProps {
  runs: TestRun[];
}

export function DurationTrendChart({ runs }: DurationTrendChartProps) {
  const data = runs
    .filter((r) => r.duration_seconds != null)
    .slice(0, 20)
    .reverse()
    .map((r) => ({
      id: r.id.slice(0, 8),
      duration: Math.round((r.duration_seconds ?? 0) * 10) / 10,
    }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="id" tick={{ fontSize: 10 }} />
        <YAxis tickFormatter={(v) => `${v}s`} tick={{ fontSize: 12 }} />
        <Tooltip formatter={(v) => [`${v}s`, "Duration"]} />
        <Area type="monotone" dataKey="duration" stroke="#8b5cf6" fill="#ede9fe" strokeWidth={2} />
      </AreaChart>
    </ResponsiveContainer>
  );
}
