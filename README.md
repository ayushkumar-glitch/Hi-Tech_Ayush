# HiTech_Ayush — Kane CLI Assurance & Evidence Demo

A Kane CLI Assurance + Evidence exercise against HiTech Digital's marketing site —
demonstrating requirement-linked test design, automated replay, and sealed evidence.

**Target application:** [hitechdigital.com](https://www.hitechdigital.com) —
main navigation, who-we-are, what-we-do services, contact lead form, direct sales contact.

## Learning objective

Demonstrate this lifecycle:

Requirement → Use Case → Acceptance Criteria → Scenario → test.md → Execution → Evidence → Coverage

## The STLC → Kane CLI mapping

| # | STLC Phase | Kane CLI Commands | What happens |
|---|-----------|-------------------|---------------|
| 1 | Requirements Analysis | `context ingest` + `context extract` | AI reads `hitech-requirements.md`, extracts cited use-cases |
| 2 | Test Planning | `context review` | Human review gate — trust or reject proposed use-cases |
| 3 | Test Design | `design tests` | AI designs acceptance criteria, scenarios, and traced `_test.md` files |
| 4 | Test Development | `testmd run` | Tests authored/replayed against a real browser session |
| 5 | Test Execution | `testrun run` | Batch replay of the committed suite with a sealed evidence pack |
| 6 | Coverage & Reporting | `evidence validate` | Integrity-checked evidence proving what's actually verified |

Phases 1–3 are run by a human, locally. Phase 4–6 are what `.github/workflows/assurance-evidence.yml`
repeats automatically on every push to `main`.

## Quick start

### 1. Clone this repo

### 2. Add secrets

**Settings → Secrets → Actions:**

| Secret | Required | Where to find it |
|--------|----------|-------------------|
| `LT_USERNAME` | Yes | accounts.lambdatest.com/security |
| `LT_ACCESS_KEY` | Yes | accounts.lambdatest.com/security |

### 3. Push to `main`

CI installs Kane CLI, replays the committed `tests/*_test.md` suite headlessly, validates the
evidence pack, and uploads it as a workflow artifact.

## Repository structure

```text
Hi-Tech_Ayush/
├── .github/
│   └── workflows/
│       └── assurance-evidence.yml      ← install kane-cli, replay committed tests, validate evidence
├── requirements/
│   └── hitech-requirements.md          ← source requirements doc (5 use-cases, 15 acceptance criteria)
├── tests/
│   ├── main-navigation-routes-to-contact-us_test.md
│   ├── main-navigation-routes-to-who-we-are_test.md
│   ├── homepage-talk-to-an-expert-cta-opens-the-contact-lead-form_test.md
│   ├── what-we-do-lists-the-required-named-services_test.md
│   ├── ai-ml-services-selection-opens-the-service-destination-page_test.md
│   └── direct-sales-contact-details-are-visible-without-form_test.md
├── .gitignore
└── README.md
```

`.testmuai/` (the local assurance store — `.context/` and sealed run packs under `evidence/`) is
intentionally excluded from git, per kane-cli guidance that the context store is append-only and
machine-specific — CI regenerates evidence on every run and publishes it as a workflow artifact
instead.

## Important design decision

The assurance design phase is intentionally performed by a human on a workstation:

1. Ingest the requirements.
2. Extract use cases.
3. Review and trust the proposed use cases.
4. Design tests.
5. Review the generated acceptance criteria, scenarios and tests.
6. Commit the reviewed `_test.md` files.

GitHub Actions then performs the repeatable execution phase:

1. Install Kane CLI.
2. Authenticate using GitHub Secrets.
3. Run the committed `_test.md` suite.
4. Validate the generated evidence pack.
5. Upload the evidence and reports as workflow artifacts.

This avoids treating the `.context/` assurance store as a Git-mergeable artifact. The Kane CLI
documentation describes `.context/` as append-only and single-writer, and recommends keeping it
out of Git merges.

**One use-case's test — subscribing to the newsletter — was intentionally excluded.** The
designed test would perform a real submission against HiTech Digital's live newsletter form,
and initial authoring showed the form requires First Name / Last Name / Industry in addition to
email, so it never actually succeeded. Rather than let a CI-triggered run retry into a real
signup, that test stays out of `tests/` (kept locally, unauthored) and out of the committed
suite. Read-only assertion coverage for that use-case's other criteria (signup field/CTA
visibility) is still exercised by design; only the actual form-submit step was cut.

## Prerequisites

- TestMu AI account with Kane CLI access.
- TestMu AI username and access key.
- Node.js 18+.
- Google Chrome for local execution.
- Git and GitHub access.

Install Kane CLI:

```bash
npm install -g @testmuai/kane-cli
```

Verify:

```bash
kane-cli --version
```

Use Kane CLI 0.6.1 or later for the assurance commands.

## Phase 1 — Local assurance design

From the repository root:

```bash
kane-cli login
```

For a non-interactive login you can use:

```bash
kane-cli login --username "<username>" --access-key "<access-key>"
```

### 1. Ingest requirements

```bash
kane-cli context ingest ./requirements/hitech-requirements.md
```

This snapshots the requirement document into the local assurance store.

### 2. Extract use cases

```bash
kane-cli context extract
```

Kane proposes use cases from the requirement document and cites the source material. Against
`hitech-requirements.md` this currently proposes five use cases covering main navigation,
the homepage lead-generation CTA, the services listing, service selection, and direct sales
contact visibility.

### 3. Review

```bash
kane-cli context review
```

Review the proposed use cases. Promote the useful ones to trusted; edit or reject proposals
where appropriate.

### 4. Design tests

For each trusted use case:

```bash
kane-cli design tests --use-case <USE_CASE_ID>
```

Review the generated acceptance criteria, scenarios and `_test.md` files. The `tests/` directory
in this repository holds the reviewed test artifacts that are actually committed and run in CI.

### 5. Review the design

```bash
kane-cli context review
```

Do not skip this step. The generated design is also derived content and should be reviewed
before becoming part of the trusted test suite.

Every test under `tests/` is requirement-linked: each `@verifies ac-N` step tag traces back to
an acceptance criterion in `requirements/hitech-requirements.md`.

## Phase 2 — Local execution

First list the tests:

```bash
kane-cli testmd list
```

Run one test:

```bash
kane-cli testmd run ./tests/main-navigation-routes-to-contact-us_test.md --agent
```

For CI-style local execution:

```bash
kane-cli testmd run ./tests/main-navigation-routes-to-contact-us_test.md \
  --agent \
  --headless \
  --on-lock-conflict wait \
  --retry
```

Run the full suite:

```bash
kane-cli testrun run ./tests \
  --agent \
  --headless \
  --on-failure fail-fast
```

A batch `testrun` produces one sealed evidence pack for the suite.

## Phase 3 — Inspect evidence

After a run, look under:

```text
.testmuai/evidence/
```

Validate the pack:

```bash
kane-cli evidence validate .testmuai/evidence/<execution-id>.evidence --json
```

Serve it locally if you want to inspect it in the evidence viewer:

```bash
kane-cli evidence serve .testmuai/evidence/<execution-id>.evidence
```

The evidence pack contains the test definitions, results, screenshots, console/network logs and
failure information.

Do not commit `.testmuai/evidence/`.

## Phase 4 — GitHub Actions

Create the following GitHub repository secrets:

- `LT_USERNAME`
- `LT_ACCESS_KEY`

Then push the repository.

The workflow in `.github/workflows/assurance-evidence.yml`:

1. Checks out the repository.
2. Installs Node.js.
3. Installs Kane CLI.
4. Logs into TestMu AI using GitHub Secrets.
5. Runs the committed HiTech tests in headless mode.
6. Validates the generated evidence pack.
7. Uploads evidence, `Result.md` files and test outputs as workflow artifacts.

## Recommended training demo

Do not make every scenario pass.

The committed suite already demonstrates this: some tests pass cleanly against the live site,
while others fail — kane-cli's own bug-detection flags whether a failure is an agent misstep in
verification or a genuine defect. Use them to walk through:

```text
Requirement
   ↓
Acceptance Criterion
   ↓
Scenario
   ↓
Test
   ↓
Execution
   ↓
Failure
   ↓
Evidence
```

Then explain the difference between:

- a product assertion that failed;
- an environment/test problem that prevented verification;
- evidence showing exactly what happened.

## Suggested training discussion

Ask the trainees:

1. Which requirement does this test prove?
2. Which acceptance criteria are covered?
3. What evidence proves the criterion?
4. If the test fails, is the product wrong or is the environment broken?
5. What remains unverified?
6. What happens to the suite if the requirement changes?

That is the core Assurance + Evidence lesson.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Workflow fails at authentication | Verify `LT_USERNAME` and `LT_ACCESS_KEY` secrets |
| Extract produces no use-cases | Check that the requirements file path is correct |
| Test authoring fails | Ensure Chrome is installed and the app URL is reachable |
| Coverage/evidence shows nothing | Run a `testrun` against the live app first |
