---
name: scrape-tenders
description: Run the PS Tender Tracker scraper (the orchestrator + adapters) without typing raw python commands. Use whenever the user wants to run, trigger, or execute the scraper / tender tracker / orchestrator / an adapter — e.g. "run the scraper", "scrape tenders", "run Adapter1", "run in prod", "scrape for 2026-07-10". Handles adapter selection, publication-anchor date, and environment (Dev/Test/Prod/Trial) switching.
---

# Scrape Tenders

Runs the PS Tender Tracker via `orchestrator.py`. The user should never need to remember the exact python invocation — translate their request into the right command using the rules below, then run it from the project root (`C:\Users\Arivazhagan\Desktop\PS-WebScrapper`).

## What the orchestrator does

`orchestrator.py` reads `adapter_config.json` (the adapter registry) and the **active** `project_config.json` (environment + notification settings), then runs each enabled adapter's 6-step pipeline and sends an email run-alert summarising the outcome.

## Step 1 — Select the environment (only if the user names one)

The active environment is whichever `project_config.json` is currently in place. To switch, copy the matching variant over it **before** running:

| User says | File to activate |
|-----------|------------------|
| dev / development (default) | `project_config_dev.json` |
| test | `project_config_test.json` |
| prod / production / live | `project_config_prod.json` |
| trial | `project_config_trial.json` |

```bash
cp project_config_<env>.json project_config.json
```

Rules:
- If the user does **not** name an environment, do **not** switch — run against whatever `project_config.json` currently holds. Confirm which environment is active by reading its `google_sheets.environment` field and stating it.
- **Prod is production and writes to the live Google Sheet.** Before running prod, confirm with the user unless they explicitly said "prod".
- After a run against a non-Dev environment, leave the config as-is (do not auto-revert) unless the user asks — but tell the user which environment is now active.

## Step 2 — Build the command

Base command (run all enabled adapters, publication anchor = today):
```bash
python orchestrator.py
```

Modifiers, combine as needed:

| User intent | Add |
|-------------|-----|
| Run only one portal — "Adapter1" / "Find a Tender" | `Adapter1` |
| Run only one portal — "Adapter2" / "Contracts Finder" | `Adapter2` |
| Specific publication anchor date | `--date YYYY-MM-DD` |

Examples:
- "run the scraper" → `python orchestrator.py`
- "run Adapter1" → `python orchestrator.py Adapter1`
- "scrape Contracts Finder for the 10th of July" → `python orchestrator.py Adapter2 --date 2026-07-10`
- "run everything in test" → `cp project_config_test.json project_config.json` then `python orchestrator.py`

The adapter argument, if present, must come **before** `--date`. Adapter IDs are case-sensitive (`Adapter1`, `Adapter2`).

## Step 3 — Run and report

Run the command from the project root. The scraper is a long-running network job (fetches the FTS/Contracts Finder OCDS API, checks each portal page, writes to Google Sheets), so allow a generous timeout (e.g. 600000 ms) and run in the background if it may exceed that.

When it finishes, report back concisely:
- Which environment and adapter(s) ran, and the publication anchor date used.
- The end-of-run summary (found / written / updated / skipped / errors) from the log output.
- Whether the run exited non-zero (a failure) — `orchestrator.py` exits 1 if any adapter failed.

## Notes & troubleshooting

- Dependencies: `pip install -r requirements.txt` (first run only). If imports like `pytz`/`holidays`/`google-*` fail, install requirements.
- Google auth: needs `credentials/credentials.json`; first run opens an OAuth flow and caches a token. `Token refresh failed` → delete `credentials/ps_tender_token.json` and re-run.
- `No tenders found` is a valid outcome (filters/date window matched nothing), not an error.
- Full logs: `tender_scraper.log` in the project root and `adapters/<adapter>/<adapter>.log`.
