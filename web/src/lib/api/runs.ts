import type { RunDetail, TestRun } from "@/types";
import { apiFetch } from "./client";

export const getRuns = (suiteId: string) =>
  apiFetch<TestRun[]>(`/api/v1/suites/${suiteId}/runs`);
export const getRun = (id: string) => apiFetch<RunDetail>(`/api/v1/runs/${id}`);
