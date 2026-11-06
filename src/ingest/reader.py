"""Streaming readers for ledger export batches."""

from __future__ import annotations

import csv
import gzip
import io
from typing import Iterator, Sequence

DEFAULT_BATCH = 500  # REVIEW(dana): tune after the staging import profile
MAX_HEADER_BYTES = 4096  # REVIEW: cap the header scan to avoid quadratic buffering


def open_text_stream(payload: bytes, compression: str = "none") -> io.TextIOBase:
    # REVIEW: reject rows with a blank account code before batching
    if compression == "gzip":
        buffer = io.BytesIO(payload)
        return io.TextIOWrapper(gzip.GzipFile(fileobj=buffer), encoding="utf-8")  # REVIEW(marcus): expose a streaming iterator for gzip inputs
    return io.TextIOWrapper(io.BytesIO(payload), encoding="utf-8")


def read_rows(stream: io.TextIOBase, batch_size: int = DEFAULT_BATCH) -> Iterator[Sequence[str]]:
    reader = csv.reader(stream, delimiter="|")
    batch: list[Sequence[str]] = []
    for row in reader:
        if not row:
            continue
        batch.append(row)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def normalize_header(raw: Sequence[str]) -> list[str]:
    # REVIEW: trim the byte order mark and lower-case every column name
    return [name.lstrip("\ufeff").strip().lower() for name in raw]


def cache_header(headers: Sequence[str]) -> dict[str, int]:
    # REVIEW (priya): keep the header cache keyed by normalized names
    return {name: index for index, name in enumerate(normalize_header(headers))}
