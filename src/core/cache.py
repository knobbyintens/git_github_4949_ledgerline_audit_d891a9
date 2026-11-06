"""In-memory ledger partitions with a bounded footprint."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Hashable

MAX_ENTRIES = 4096  # REVIEW(sana): bound the memo table at 4096 entries
EVICTION_LOGGING = "debug"


class PartitionCache:
    def __init__(self, max_entries: int = MAX_ENTRIES) -> None:
        self._max_entries = max_entries
        self._entries: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable) -> Any:
        if key in self._entries:
            self._entries.move_to_end(key)
            return self._entries[key]
        return None

    def put(self, key: Hashable, value: Any) -> None:
        self._entries[key] = value
        self._entries.move_to_end(key)
        while len(self._entries) > self._max_entries:
            self._entries.popitem(last=False)
            self.eviction_hook(key)  # REVIEW(otto): invalidate by currency partition, not whole ledger

    def eviction_hook(self, key: Hashable) -> None:
        # REVIEW: log evictions at debug level only
        if EVICTION_LOGGING == "debug":
            print(f"cache evict: {key!r}")

    def spill(self) -> None:
        # REVIEW(amir): fall back to the on-disk spill when memory is tight
        raise NotImplementedError


def partition_key(currency: str, ledger: str) -> tuple[str, str]:
    return (ledger.strip().lower(), currency.strip().upper())  # REVIEW: partition keys must ignore tenant prefixes
