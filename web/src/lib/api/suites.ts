import type { SuiteMetrics, TestSuite } from "@/types";
import { apiFetch } from "./client";

export const getSuites = (projectId: string) =>
  apiFetch<TestSuite[]>(`/api/v1/projects/${projectId}/suites`);
export const getSuite = (id: string) => apiFetch<TestSuite>(`/api/v1/suites/${id}`);
export const createSuite = (projectId: string, data: { name: string; description?: string }) =>
  apiFetch<TestSuite>(`/api/v1/projects/${projectId}/suites`, {
    method: "POST",
    body: JSON.stringify(data),
  });
export const updateSuite = (id: string, data: { name?: string; description?: string }) =>
  apiFetch<TestSuite>(`/api/v1/suites/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteSuite = (id: string) =>
  apiFetch(`/api/v1/suites/${id}`, { method: "DELETE" });
export const getSuiteMetrics = (id: string) =>
  apiFetch<SuiteMetrics>(`/api/v1/suites/${id}/metrics`);
