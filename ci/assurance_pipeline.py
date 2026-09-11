#!/usr/bin/env python3
"""
Assurance pipeline orchestrator.

Drives the kane-cli assurance journey end-to-end in CI:
  ingest -> extract -> (auto-approve) review -> design -> (auto-approve) review
  -> author (testmd run) -> replay (testrun run) -> cover gaps

Each stage's raw NDJSON is written under artifacts/ for debugging; a plain-language
summary is printed to stdout and appended to $GITHUB_STEP_SUMMARY when present.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)

PRD_PATH = os.environ.get("PRD_PATH", "requirements/prd.md")
DESIGN_MAX = os.environ.get("DESIGN_MAX", "8")
AUTO_APPROVE = os.environ.get("AUTO_APPROVE", "true").lower() == "true"


def step_summary(text: str) -> None:
    print(text)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write(text + "\n")


def run(cmd: list[str], log_name: str, allow_exit: tuple[int, ...] = (0,)) -> tuple[int, list[dict]]:
    print(f"$ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    log_path = ARTIFACTS / log_name
    log_path.write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr)
    events = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if proc.returncode not in allow_exit:
        step_summary(f"❌ `{cmd[1]}` failed (exit {proc.returncode}) — see `{log_name}`")
        print(proc.stderr, file=sys.stderr)
        sys.exit(proc.returncode)
    return proc.returncode, events


def approve_all_pending(kind: str) -> None:
    """Build verdicts approving every pending item and land them (checkpoint)."""
    if not AUTO_APPROVE:
        step_summary(f"⏸️  {kind} checkpoint: AUTO_APPROVE=false — leaving items queued for manual review.")
        return

    code, events = run(
        ["kane-cli", "context", "list", "--json", "--inferred"],
        f"{kind}_pending.ndjson",
    )
    # `context list --json` prints one JSON row per line (not wrapped in run/done events).
    pending = [e for e in events if e.get("status") in (None, "derived", "pending")]
    if not pending:
        step_summary(f"✅ No pending {kind} items to review.")
        return

    verdicts = [{"ref": item["ref"], "resolution": "approved"} for item in pending if "ref" in item]
    if not verdicts:
        step_summary(f"✅ No pending {kind} items to review.")
        return

    verdicts_path = ARTIFACTS / f"{kind}_verdicts.json"
    verdicts_path.write_text(json.dumps(verdicts, indent=2))
    run(["kane-cli", "context", "review", "--verdicts", str(verdicts_path), "--json"], f"{kind}_review.ndjson")
    step_summary(f"✅ Auto-approved {len(verdicts)} {kind} item(s) (recommended defaults).")


def main() -> None:
    step_summary("## Assurance Pipeline\n")

    # 1. Ingest requirements + extract use-cases
    run(["kane-cli", "context", "ingest", PRD_PATH, "--mode", "agent"], "01_ingest.ndjson", allow_exit=(0, 3))

    # 2. Checkpoint: approve extracted use-cases
    approve_all_pending("use-case")

    # 3. Design tests from the trusted use-case(s)
    code, events = run(
        ["kane-cli", "context", "list", "--json"],
        "02_list_usecases.ndjson",
    )
    use_case_refs = [e["ref"] for e in events if e.get("kind") == "use_case" and e.get("trust") == "trusted"]
    if not use_case_refs:
        step_summary("❌ No trusted use-cases found after review — cannot design tests.")
        sys.exit(1)

    for uc_ref in use_case_refs:
        run(
            ["kane-cli", "design", "tests", "--use-case", uc_ref, "--mode", "agent", "--max", DESIGN_MAX],
            f"03_design_{uc_ref}.ndjson",
            allow_exit=(0, 3),
        )

    # 4. Checkpoint: approve the designed tests
    approve_all_pending("design")

    # 5. Author each designed test in a real browser
    tests_dir = ROOT / ".testmuai" / "tests"
    test_files = sorted(tests_dir.glob("*_test.md")) if tests_dir.exists() else []
    if not test_files:
        step_summary("❌ No designed tests found under .testmuai/tests/ — nothing to author.")
        sys.exit(1)

    for test_file in test_files:
        run(["kane-cli", "testmd", "run", str(test_file), "--agent"], f"04_author_{test_file.stem}.ndjson")

    # 6. Batch-replay the authored suite
    run(["kane-cli", "testrun", "run", "--match", "t-"], "05_testrun.ndjson")

    step_summary(f"\n✅ Authored and replayed {len(test_files)} test(s).")


if __name__ == "__main__":
    main()
