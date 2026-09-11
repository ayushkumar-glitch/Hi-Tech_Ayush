# HiTech_Ayush — Assurance & Evidence CI with kane-cli

**Problem statement:** Create a GitHub Actions workflow with kane-cli covering assurance and
evidence.

This repo wires kane-cli's **assurance** pipeline (requirement-linked test design + coverage
accounting) and **evidence** packs (sealed, validated run artifacts) into a GitHub Actions
workflow, following the flow documented in
[gagan-lambda/agentic-sdlc-pitch](https://github.com/gagan-lambda/agentic-sdlc-pitch):
requirements in → tests designed and authored → replayed → coverage and evidence published.

## What the workflow does

`.github/workflows/assurance-evidence.yml` (manual dispatch only, to avoid burning credits on
every commit):

1. **Ingest** `requirements/prd.md` and extract use-cases (`kane-cli context ingest`).
2. **Checkpoint 1** — auto-approve extracted use-cases with recommended defaults (toggle via
   the `auto_approve` input).
3. **Design** tests against each trusted use-case (`kane-cli design tests --max 8`), writing
   requirement-linked tests under `.testmuai/tests/*_test.md`, each step tagged with the
   acceptance criteria it verifies.
4. **Checkpoint 2** — auto-approve the designed tests.
5. **Author** each designed test in a real browser (`kane-cli testmd run`).
6. **Replay** the authored suite as a batch (`kane-cli testrun run`).
7. **Publish coverage** — `kane-cli cover gaps --json` rendered as a traceability matrix
   (AC → use-case → test → designed %/proven %) in the GitHub Step Summary.
8. **Validate & upload evidence** — every sealed `.evidence` pack is checked with
   `kane-cli evidence validate` and uploaded as a downloadable Actions artifact, alongside the
   designed tests and raw pipeline logs.

## Repository structure

```
├── .github/workflows/
│   └── assurance-evidence.yml   # the CI workflow
├── ci/
│   ├── assurance_pipeline.py    # ingest -> extract -> design -> author -> replay
│   ├── traceability.py          # cover gaps -> AC/use-case/test matrix -> step summary
│   └── evidence.py              # validate .evidence packs -> step summary
├── requirements/
│   └── prd.md                   # the requirements document kane-cli ingests
├── scenarios/                   # (populated by design tests, gitignored output lands in .testmuai/)
├── tests/                       # place for hand-curated fixtures, if any (tests themselves are authored, not written by hand)
├── requirements.txt
└── README.md
```

`.context/` (the assurance store) and `.testmuai/` (designed tests + sealed evidence) are
local/CI-generated and gitignored — they're published as workflow artifacts instead of
committed.

## GitHub Secrets required

| Secret | Source |
|---|---|
| `LT_USERNAME` | accounts.lambdatest.com/security |
| `LT_ACCESS_KEY` | accounts.lambdatest.com/security |
| `ANTHROPIC_API_KEY` | console.anthropic.com |

## Workflow inputs

| Input | Required | Purpose |
|---|---|---|
| `tm_project_id` | ✅ | Test Manager project ID |
| `tm_environment_id` | optional | Test environment ID |
| `kane_folder_id` | recommended | KaneAI folder ID for saving authored tests |
| `prd_path` | optional (default `requirements/prd.md`) | Requirements document to ingest |
| `design_max` | optional (default `8`) | Max scenario+test pairs per use-case |
| `auto_approve` | optional (default `true`) | Auto-approve assurance checkpoints with recommended defaults |

## Local execution

```bash
npm install -g @testmuai/kane-cli@latest
pip install -r requirements.txt
kane-cli login --username $LT_USERNAME --access-key $LT_ACCESS_KEY
kane-cli config project YOUR_TM_PROJECT_ID

PRD_PATH=requirements/prd.md DESIGN_MAX=8 AUTO_APPROVE=true python3 ci/assurance_pipeline.py
python3 ci/traceability.py
python3 ci/evidence.py
```

## Design notes

- **Manual dispatch only:** assurance (`context extract`, `design tests`) and authoring
  (`testmd run`) calls consume kane-cli credits — this must not auto-trigger on every push.
- **Two checkpoints, auto-approvable in CI:** the assurance journey has two human-review
  checkpoints (use-case approval, design approval). In CI these default to auto-approving the
  tool's recommended verdicts (`auto_approve: true`); set it to `false` to leave items queued
  for a human to review with `kane-cli context review` locally.
- **Traceability over raw counts:** every test kane-cli designs is permanently tagged with the
  acceptance criteria it verifies, so the coverage step surfaces AC → use-case → test → result,
  not just a pass/fail count.
- **Evidence, not just logs:** every run seals an `.evidence` pack (screenshots, console/network
  logs, failure records). The workflow validates each pack's integrity before publishing it, so
  a broken/truncated pack fails the run instead of silently uploading garbage.
