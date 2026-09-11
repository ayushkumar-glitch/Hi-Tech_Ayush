#!/usr/bin/env python3
"""
Publishes the AC -> use-case -> test -> result traceability matrix and coverage
ribbon (kane-cli cover gaps) to the GitHub Step Summary.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def step_summary(text: str) -> None:
    print(text)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write(text + "\n")


def main() -> None:
    proc = subprocess.run(
        ["kane-cli", "cover", "gaps", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    (ARTIFACTS / "cover_gaps.json").write_text(proc.stdout)

    if proc.returncode != 0:
        step_summary(f"⚠️ `kane-cli cover gaps --json` exited {proc.returncode}; raw output saved to artifacts/cover_gaps.json")
        print(proc.stderr, file=sys.stderr)
        return

    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError:
        step_summary("⚠️ Could not parse `cover gaps --json` output; see artifacts/cover_gaps.json")
        return

    step_summary("\n## Traceability Matrix\n")
    step_summary("| Use Case | Acceptance Criteria | Designed % | Proven % | Pending |")
    step_summary("|---|---|---|---|---|")

    for uc in doc.get("use_cases", doc.get("rows", [])):
        name = uc.get("title") or uc.get("id") or uc.get("use_case_id", "unknown")
        acs = uc.get("acceptance_criteria", uc.get("acs", []))
        ac_text = ", ".join(a.get("id", str(a)) if isinstance(a, dict) else str(a) for a in acs) or "—"
        designed = uc.get("designed_pct", uc.get("designed", "—"))
        proven = uc.get("proven_pct", uc.get("proven", "—"))
        pending = uc.get("pending_count", len(uc.get("pending", [])))
        step_summary(f"| {name} | {ac_text} | {designed} | {proven} | {pending} |")

    step_summary(f"\nFull JSON: `artifacts/cover_gaps.json`")


if __name__ == "__main__":
    main()
