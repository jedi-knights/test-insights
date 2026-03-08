export enum BuildSystem {
  GITHUB_ACTIONS = "github_actions",
  GITLAB_CI = "gitlab_ci",
  JENKINS = "jenkins",
  CIRCLECI = "circleci",
  LOCAL = "local",
  UNKNOWN = "unknown",
}

export enum RunStatus {
  RUNNING = "running",
  PASSED = "passed",
  FAILED = "failed",
  ERROR = "error",
}

export enum CaseStatus {
  PASSED = "passed",
  FAILED = "failed",
  ERROR = "error",
  SKIPPED = "skipped",
}

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
}

export interface Team {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  team_id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface TestSuite {
  id: string;
  project_id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface TestRun {
  id: string;
  suite_id: string;
  build_system: BuildSystem;
  branch: string | null;
  commit_sha: string | null;
  status: RunStatus;
  total_tests: number;
  passed_tests: number;
  failed_tests: number;
  skipped_tests: number;
  error_tests: number;
  duration_seconds: number | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  metadata: Record<string, unknown>;
}

export interface TestCase {
  id: string;
  run_id: string;
  name: string;
  classname: string | null;
  file_path: string | null;
  status: CaseStatus;
  duration_seconds: number | null;
  error_message: string | null;
  stack_trace: string | null;
  created_at: string;
}

export interface RunDetail {
  run: TestRun;
  cases: TestCase[];
}

export interface PassRatePoint {
  date: string;
  pass_rate: number;
  total: number;
}

export interface TeamMetrics {
  team_id: string;
  total_projects: number;
  total_suites: number;
  total_runs: number;
  overall_pass_rate: number;
  pass_rate_trend: PassRatePoint[];
}

export interface ProjectMetrics {
  project_id: string;
  total_suites: number;
  total_runs: number;
  overall_pass_rate: number;
  pass_rate_trend: PassRatePoint[];
}

export interface SuiteMetrics {
  suite_id: string;
  total_runs: number;
  overall_pass_rate: number;
  pass_rate_trend: PassRatePoint[];
}
