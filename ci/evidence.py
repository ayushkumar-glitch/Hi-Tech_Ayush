#!/usr/bin/env python3
"""
Validates every sealed evidence pack produced this run and writes a summary table.
Packs live under .testmuai/evidence/ per kane-cli's evidence layout.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / ".testmuai" / "evidence"
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def step_summary(text: str) -> None:
    print(text)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write(text + "\n")


def main() -> None:
    step_summary("\n## Evidence Packs\n")

    if not EVIDENCE_DIR.exists():
        step_summary("⚠️ No `.testmuai/evidence/` directory found — no packs were sealed this run.")
        return

    packs = sorted(EVIDENCE_DIR.glob("*.evidence"))
    if not packs:
        step_summary("⚠️ No `.evidence` packs found.")
        return

    step_summary("| Pack | Valid | Notes |")
    step_summary("|---|---|---|")

    any_invalid = False
    for pack in packs:
        proc = subprocess.run(
            ["kane-cli", "evidence", "validate", str(pack), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        valid = proc.returncode == 0
        any_invalid = any_invalid or not valid
        note = "" if valid else f"exit {proc.returncode}"
        step_summary(f"| `{pack.name}` | {'✅' if valid else '❌'} | {note} |")
        (ARTIFACTS / f"{pack.stem}.validate.json").write_text(proc.stdout or proc.stderr)

    step_summary(f"\n{len(packs)} pack(s) checked. Download the `evidence-packs` artifact for full replay data.")

    if any_invalid:
        sys.exit(1)


if __name__ == "__main__":
    main()
