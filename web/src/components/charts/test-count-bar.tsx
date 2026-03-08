"use client";

import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { TestRun } from "@/types";

interface TestCountBarProps {
  runs: TestRun[];
}

export function TestCountBar({ runs }: TestCountBarProps) {
  const data = runs.slice(0, 20).reverse().map((r) => ({
    id: r.id.slice(0, 8),
    passed: r.passed_tests,
    failed: r.failed_tests,
    skipped: r.skipped_tests,
    error: r.error_tests,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="id" tick={{ fontSize: 10 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip />
        <Legend />
        <Bar dataKey="passed" stackId="a" fill="#22c55e" />
        <Bar dataKey="failed" stackId="a" fill="#ef4444" />
        <Bar dataKey="skipped" stackId="a" fill="#94a3b8" />
        <Bar dataKey="error" stackId="a" fill="#f97316" />
      </BarChart>
    </ResponsiveContainer>
  );
}
