# HiTech_Ayush — Assurance & Evidence CI with kane-cli

**Problem statement:** Create a GitHub Actions workflow with kane-cli covering assurance and
evidence.

This repo applies kane-cli's Assurance + Evidence lifecycle — Requirement → Use Case →
Acceptance Criteria → Scenario → test.md → Execution → Evidence → Coverage — to
[hitechdigital.com](https://www.hitechdigital.com)

> **Human performs the design phase locally** (ingestion, extraction, review, test design).
> **GitHub Actions handles repeatable execution** (installation, authentication, test runs,
> evidence validation, artifact uploads).

## Repository structure

```
├── .github/workflows/
│   └── assurance-evidence.yml   # CI: install kane-cli, replay committed tests, validate evidence
├── requirements/
│   └── hitech-requirements.md   # source requirements doc (5 use-cases, 15 acceptance criteria)
├── tests/
│   ├── main-navigation-routes-to-contact-us_test.md
│   ├── main-navigation-routes-to-who-we-are_test.md
│   ├── homepage-talk-to-an-expert-cta-opens-the-contact-lead-form_test.md
│   ├── what-we-do-lists-the-required-named-services_test.md
│   ├── ai-ml-services-selection-opens-the-service-destination-page_test.md
│   └── direct-sales-contact-details-are-visible-without-form_test.md
└── README.md
```

`.testmuai/` (containing `.context/`, the local assurance store, and `evidence/`, sealed run
packs) is intentionally excluded from git, per kane-cli guidance that the context store is
append-only and machine-specific — CI regenerates evidence on every run and publishes it as a
workflow artifact instead.

## How the tests were designed (local, one-time)

```bash
npm install -g @testmuai/kane-cli@latest
kane-cli login --username $LT_USERNAME --access-key $LT_ACCESS_KEY

kane-cli context ingest requirements/hitech-requirements.md --mode agent   # extract use-cases
kane-cli context review --verdicts verdicts.json --json                   # approve use-cases
kane-cli design tests --use-case uc-1 --mode agent --max 3                # design ACs/scenarios/tests
kane-cli context review --verdicts verdicts.json --json                   # approve the design
kane-cli testmd run tests/<name>_test.md --agent --headless               # author in a real browser
```

Every test under `tests/` is requirement-linked: each `@verifies ac-N` step tag traces back to
an acceptance criterion in `requirements/hitech-requirements.md`.

**One use-case's test — subscribing to the newsletter — was intentionally excluded.** The
designed test would perform a real submission against HiTech Digital's live newsletter form,
and initial authoring showed the form requires First Name / Last Name / Industry in addition to
email, so it never actually succeeded. Rather than let a CI-triggered run retry into a real
signup, that test stays out of `tests/` (kept locally, unauthored) and out of the committed
suite. Read-only assertion coverage for that use-case's other criteria (signup field/CTA
visibility) is still exercised by design; only the actual form-submit step was cut.

## What CI does

`.github/workflows/assurance-evidence.yml` — runs on push to `main` (and manual dispatch):

1. Install Node.js 20 and `@testmuai/kane-cli`.
2. Authenticate with `LT_USERNAME` / `LT_ACCESS_KEY` secrets.
3. `kane-cli testrun run tests/*_test.md --headless` — replays the 6 committed tests as one batch.
4. `kane-cli evidence validate` — integrity-checks every sealed `.evidence` pack.
5. Uploads `evidence-packs` and `test-results` as downloadable workflow artifacts.

## GitHub Secrets required

| Secret | Source |
|---|---|
| `LT_USERNAME` | accounts.lambdatest.com/security |
| `LT_ACCESS_KEY` | accounts.lambdatest.com/security |

## Local execution

```bash
npm install -g @testmuai/kane-cli
kane-cli login --username $LT_USERNAME --access-key $LT_ACCESS_KEY
kane-cli testrun run tests/*_test.md --headless
kane-cli evidence validate .testmuai/evidence/<id>.evidence --json
kane-cli evidence serve .testmuai/evidence/<id>.evidence   # view results in a browser
```
