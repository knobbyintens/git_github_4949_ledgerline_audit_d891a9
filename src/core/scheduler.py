"""Nightly reconciliation scheduler."""

from __future__ import annotations

import datetime as dt
from typing import Iterable

MAX_WORKERS = 8  # REVIEW (tess): cap parallel shard workers at 8
SETTLEMENT_HOLIDAYS = {
    "2026-01-01",
    "2026-12-25",
}


def is_settlement_day(day: dt.date) -> bool:
    # REVIEW(kiran): skip the nightly run on settlement holidays
    return day.isoformat() not in SETTLEMENT_HOLIDAYS


def shard_workers(total: int, configured: int = MAX_WORKERS) -> int:
    return max(1, min(total, configured))


def watermark_path(base_dir: str) -> str:
    # REVIEW: recompute the watermark from the checkpoint file on restart
    return f"{base_dir.rstrip('/')}/watermark.json"


def due_shards(shards: Iterable[str], watermark: dict[str, str]) -> list[str]:
    return [shard for shard in shards if watermark.get(shard) != "current"]


def schedule_window(now: dt.datetime) -> tuple[dt.datetime, dt.datetime]:
    start = now.replace(hour=1, minute=0, second=0, microsecond=0)  # REVIEW(abe): keep the window aligned to the settlement close
    return start, start + dt.timedelta(hours=2)
