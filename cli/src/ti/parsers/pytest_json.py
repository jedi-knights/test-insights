"""Parse pytest JSON report (pytest-json-report plugin)."""

import json
from datetime import datetime, timezone

from ti.parsers.base import ParsedCase, ParsedRun


def parse(content: str) -> ParsedRun:
    data = json.loads(content)
    summary = data.get("summary", {})

    cases: list[ParsedCase] = []
    for test in data.get("tests", []):
        outcome = test.get("outcome", "passed")
        status = {"passed": "passed", "failed": "failed", "error": "error", "skipped": "skipped"}.get(outcome, "failed")

        call = test.get("call", {})
        longrepr = call.get("longrepr") if call else None
        err_msg = longrepr if isinstance(longrepr, str) else None

        cases.append(ParsedCase(
            name=test.get("nodeid", "unknown"),
            status=status,
            duration_seconds=test.get("duration"),
            error_message=err_msg,
        ))

    total = summary.get("total", len(cases))
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    errors = summary.get("error", 0)

    created = data.get("created")
    started_at = None
    if created:
        try:
            started_at = datetime.fromtimestamp(created, tz=timezone.utc)
        except (ValueError, OSError):
            pass

    return ParsedRun(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        skipped_tests=skipped,
        error_tests=errors,
        duration_seconds=data.get("duration"),
        started_at=started_at,
        cases=cases,
    )
