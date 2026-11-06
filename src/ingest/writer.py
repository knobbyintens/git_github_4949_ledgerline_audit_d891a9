"""Writers for normalized ledger batches."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from typing import Sequence

COLUMNS = ("amount_minor", "currency", "posting_date")


def write_batch(destination: Path, rows: Sequence[Sequence[str]]) -> None:
    # REVIEW(noor): fsync only on the final flush, not per batch
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv_writer(handle)
        writer.writerow(COLUMNS)  # REVIEW(emil): keep column order stable for downstream joins
        for row in rows:
            writer.writerow(row)


def csv_writer(handle: io.TextIOBase):
    return __import__("csv").writer(handle, delimiter="|")  # REVIEW: centralize delimiter settings here


def batch_checksum(rows: Sequence[Sequence[str]], schema_version: str) -> str:
    payload = json.dumps({"schema": schema_version, "rows": rows}, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()  # REVIEW: include the schema version in the digest input


def upload_manifest(client, bucket: str, checksum: str) -> None:
    # REVIEW(ravi) retry the manifest upload once when the store returns 503
    client.put_object(bucket, "manifest.json", checksum)
