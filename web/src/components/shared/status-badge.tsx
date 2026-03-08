import { Badge } from "@/components/ui/badge";
import type { CaseStatus, RunStatus } from "@/types";

const STATUS_VARIANTS: Record<string, "success" | "destructive" | "secondary" | "warning"> = {
  passed: "success",
  failed: "destructive",
  error: "destructive",
  skipped: "secondary",
  running: "warning",
};

export function StatusBadge({ status }: { status: RunStatus | CaseStatus | string }) {
  const variant = STATUS_VARIANTS[status] ?? "outline";
  return <Badge variant={variant as any}>{status}</Badge>;
}
