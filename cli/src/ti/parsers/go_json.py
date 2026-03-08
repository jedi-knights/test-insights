"""Parse Go test JSON output (go test -json)."""

import json
from datetime import datetime, timezone

from ti.parsers.base import ParsedCase, ParsedRun


def parse(content: str) -> ParsedRun:
    events: list[dict] = []
    for line in content.splitlines():
        line = line.strip()
        if line:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    # Collect per-test outcomes
    tests: dict[str, dict] = {}
    output_buf: dict[str, list[str]] = {}

    for event in events:
        action = event.get("Action")
        test = event.get("Test")
        if not test:
            continue

        key = f"{event.get('Package', '')}/{test}"
        if action == "run":
            tests[key] = {"name": test, "package": event.get("Package", ""), "status": "running", "elapsed": None}
            output_buf[key] = []
        elif action in ("pass", "fail", "skip"):
            if key not in tests:
                tests[key] = {"name": test, "package": event.get("Package", ""), "status": "running", "elapsed": None}
            status = {"pass": "passed", "fail": "failed", "skip": "skipped"}.get(action, "failed")
            tests[key]["status"] = status
            tests[key]["elapsed"] = event.get("Elapsed")
        elif action == "output" and key in output_buf:
            output_buf[key].append(event.get("Output", ""))

    cases: list[ParsedCase] = []
    passed = failed = skipped = errors = 0

    for key, info in tests.items():
        status = info["status"]
        if status == "passed":
            passed += 1
        elif status == "failed":
            failed += 1
        elif status == "skipped":
            skipped += 1

        output = "".join(output_buf.get(key, []))
        cases.append(ParsedCase(
            name=info["name"],
            classname=info.get("package"),
            status=status,
            duration_seconds=info.get("elapsed"),
            error_message=output if status in ("failed", "error") else None,
        ))

    # Try to get started_at from first event timestamp
    started_at = None
    for event in events:
        if event.get("Time"):
            try:
                started_at = datetime.fromisoformat(event["Time"].replace("Z", "+00:00"))
            except ValueError:
                pass
            break

    total = len(cases)
    return ParsedRun(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        skipped_tests=skipped,
        error_tests=errors,
        duration_seconds=None,
        started_at=started_at,
        cases=cases,
    )
