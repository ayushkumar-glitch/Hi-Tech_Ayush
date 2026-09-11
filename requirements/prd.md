# Problem Statement

Create a GitHub Actions workflow with kane-cli covering **assurance** and **evidence**.

## Acceptance Criteria

- AC-1: The repository ships a requirements document (this file) that kane-cli's assurance
  pipeline can ingest to derive use-cases and acceptance criteria.
- AC-2: A GitHub Actions workflow exists that, on manual dispatch, runs the full kane-cli
  assurance journey: ingest → extract → design → author → replay.
- AC-3: The workflow produces requirement-linked test cases (each test tagged with the
  acceptance criteria it verifies) under `.testmuai/tests/`.
- AC-4: The workflow computes and publishes coverage (`kane-cli cover gaps`) as a GitHub
  Step Summary, showing designed % and proven % per use-case.
- AC-5: The workflow seals and validates evidence packs (`kane-cli evidence validate`) for
  every executed test and uploads them as a downloadable GitHub Actions artifact.
- AC-6: Evidence and coverage results are traceable back to the acceptance criteria in this
  document (AC -> use-case -> test -> result).
- AC-7: The workflow is manually triggered (`workflow_dispatch`) to avoid unnecessary credit
  consumption on every commit.

## Use Case: Assurance-driven CI pipeline

As an engineer, I want a GitHub Actions workflow that uses kane-cli's assurance commands to
design tests from this PRD, execute them, and publish coverage + evidence, so that every CI
run answers "what is covered, and how do we know?" with citable proof.

### Flow

1. Ingest this PRD (`kane-cli context ingest requirements/prd.md --mode agent`).
2. Review/auto-approve the extracted use-cases (assurance checkpoint 1).
3. Design tests against the approved use-case (`kane-cli design tests --mode agent --max 8`).
4. Review/auto-approve the designed tests (assurance checkpoint 2).
5. Author each designed test in a real browser (`kane-cli testmd run`).
6. Batch-replay the authored suite (`kane-cli testrun run`).
7. Compute coverage (`kane-cli cover gaps`) and publish it as a traceability matrix.
8. Validate and upload evidence packs (`kane-cli evidence validate`, `actions/upload-artifact`).
