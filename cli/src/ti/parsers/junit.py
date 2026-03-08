"""Parse JUnit XML test reports."""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from ti.parsers.base import ParsedCase, ParsedRun


def parse(content: str) -> ParsedRun:
    root = ET.fromstring(content)
    # Handle both <testsuite> and <testsuites> root elements
    if root.tag == "testsuites":
        suites = list(root.iter("testsuite"))
    else:
        suites = [root]

    cases: list[ParsedCase] = []
    total = passed = failed = skipped = errors = 0
    total_duration = 0.0
    started_at: datetime | None = None

    for suite in suites:
        for tc in suite.iter("testcase"):
            name = tc.get("name", "unknown")
            classname = tc.get("classname")
            duration = float(tc.get("time", 0) or 0)

            failure = tc.find("failure")
            error = tc.find("error")
            skip = tc.find("skipped")

            if skip is not None:
                status = "skipped"
                skipped += 1
                err_msg = None
                stack = None
            elif failure is not None:
                status = "failed"
                failed += 1
                err_msg = failure.get("message")
                stack = failure.text
            elif error is not None:
                status = "error"
                errors += 1
                err_msg = error.get("message")
                stack = error.text
            else:
                status = "passed"
                passed += 1
                err_msg = None
                stack = None

            total += 1
            total_duration += duration

            cases.append(ParsedCase(
                name=name,
                classname=classname,
                status=status,
                duration_seconds=duration if duration else None,
                error_message=err_msg,
                stack_trace=stack,
            ))

        ts = suite.get("timestamp")
        if ts and not started_at:
            try:
                started_at = datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)
            except ValueError:
                pass

    return ParsedRun(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        skipped_tests=skipped,
        error_tests=errors,
        duration_seconds=total_duration if total_duration else None,
        started_at=started_at,
        cases=cases,
    )
