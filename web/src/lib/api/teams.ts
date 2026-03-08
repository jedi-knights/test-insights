import type { Team, TeamMetrics } from "@/types";
import { apiFetch } from "./client";

export const getTeams = () => apiFetch<Team[]>("/api/v1/teams");
export const getTeam = (id: string) => apiFetch<Team>(`/api/v1/teams/${id}`);
export const createTeam = (data: { name: string; description?: string }) =>
  apiFetch<Team>("/api/v1/teams", { method: "POST", body: JSON.stringify(data) });
export const updateTeam = (id: string, data: { name?: string; description?: string }) =>
  apiFetch<Team>(`/api/v1/teams/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteTeam = (id: string) =>
  apiFetch(`/api/v1/teams/${id}`, { method: "DELETE" });
export const getTeamMetrics = (id: string) =>
  apiFetch<TeamMetrics>(`/api/v1/teams/${id}/metrics`);
