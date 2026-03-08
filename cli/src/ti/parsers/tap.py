"""Parse TAP (Test Anything Protocol) output."""

import re

from ti.parsers.base import ParsedCase, ParsedRun


def parse(content: str) -> ParsedRun:
    cases: list[ParsedCase] = []
    passed = failed = skipped = 0
    ok_pat = re.compile(r"^(ok|not ok)\s+(\d+)(?:\s+-\s+(.*))?$")

    for line in content.splitlines():
        m = ok_pat.match(line.strip())
        if not m:
            continue
        result, num, description = m.groups()
        description = description or f"Test {num}"
        directive = ""
        if description:
            dir_match = re.search(r"#\s*(skip|todo)\s*(.*)", description, re.IGNORECASE)
            if dir_match:
                directive = dir_match.group(1).lower()
                description = description[:dir_match.start()].strip()

        if directive == "skip":
            status = "skipped"
            skipped += 1
        elif result == "ok":
            status = "passed"
            passed += 1
        else:
            status = "failed"
            failed += 1

        cases.append(ParsedCase(name=description, status=status))

    total = len(cases)
    return ParsedRun(
        total_tests=total,
        passed_tests=passed,
        failed_tests=failed,
        skipped_tests=skipped,
        error_tests=0,
        duration_seconds=None,
        started_at=None,
        cases=cases,
    )
