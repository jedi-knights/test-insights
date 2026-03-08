import type { Project, ProjectMetrics } from "@/types";
import { apiFetch } from "./client";

export const getProjects = (teamId: string) =>
  apiFetch<Project[]>(`/api/v1/teams/${teamId}/projects`);
export const getProject = (id: string) => apiFetch<Project>(`/api/v1/projects/${id}`);
export const createProject = (teamId: string, data: { name: string; description?: string }) =>
  apiFetch<Project>(`/api/v1/teams/${teamId}/projects`, {
    method: "POST",
    body: JSON.stringify(data),
  });
export const updateProject = (id: string, data: { name?: string; description?: string }) =>
  apiFetch<Project>(`/api/v1/projects/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteProject = (id: string) =>
  apiFetch(`/api/v1/projects/${id}`, { method: "DELETE" });
export const getProjectMetrics = (id: string) =>
  apiFetch<ProjectMetrics>(`/api/v1/projects/${id}/metrics`);
