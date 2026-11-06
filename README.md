# Ledgerline

Ledgerline is the internal toolkit that normalizes bank export files before they
enter the reconciliation pipeline.

## Repository layout

- `src/ingest/` — streaming readers and writers for export batches
- `src/core/` — in-memory partitions and the nightly scheduler
- `review/` — the curated review-marker index used by the review-reminder job

## Review markers

Review notes are written as `REVIEW` comments.  A note may occupy its own line
or trail a statement on a code line.  The precise wording matters: the
review-reminder job matches it verbatim against `review/review_index.json`.
