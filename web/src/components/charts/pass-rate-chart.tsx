"use client";

import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { PassRatePoint } from "@/types";

interface PassRateChartProps {
  data: PassRatePoint[];
}

export function PassRateChart({ data }: PassRateChartProps) {
  const formatted = data.map((d) => ({
    date: d.date,
    passRate: Math.round(d.pass_rate * 100),
    total: d.total,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={formatted} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 100]} tickFormatter={(v) => `${v}%`} tick={{ fontSize: 12 }} />
        <Tooltip formatter={(value) => [`${value}%`, "Pass Rate"]} />
        <Line type="monotone" dataKey="passRate" stroke="#3b82f6" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
