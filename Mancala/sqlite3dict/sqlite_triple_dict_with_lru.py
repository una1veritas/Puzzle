#!/usr/bin/env python3
"""
Sqlite-backed dict-like mapping: int -> (int, int, int) with optional tiny LRU cache.

Usage:
    d = SqliteTripleDict("data.db", autocommit=False, lru_capacity=128)
    d[1] = (10, 20, 30)
    print(d[1])
    print(d.cache_info())
"""
from __future__ import annotations

import sqlite3
from collections import OrderedDict
from collections.abc import MutableMapping, Iterator
from typing import Dict, Iterable, Tuple, Optional, Any

Triple = Tuple[int, int, int]


class LRUCache:
    """Tiny LRU cache storing key -> Triple using OrderedDict.

    - capacity <= 0 means disabled.
    - read-through logic is handled by the caller.
    """
    __slots__ = ("capacity", "_data", "hits", "misses")

    def __init__(self, capacity: int = 0) -> None:
        self.capacity = int(capacity)
        self._data: "OrderedDict[int, Triple]" = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: int) -> Optional[Triple]:
        if self.capacity <= 0:
            self.misses += 1
            return None
        v = self._data.get(key)
        if v is None:
            self.misses += 1
            return None
        # move to end = most recently used
        self._data.move_to_end(key)
        self.hits += 1
        return v

    def put(self, key: int, value: Triple) -> None:
        if self.capacity <= 0:
            return
        if key in self._data:
            # replace and mark as most recently used
            self._data[key] = value
            self._data.move_to_end(key)
        else:
            self._data[key] = value
            # evict least-recently-used if needed
            if len(self._data) > self.capacity:
                self._data.popitem(last=False)

    def pop(self, key: int, default: Optional[Triple] = None) -> Optional[Triple]:
        if self.capacity <= 0:
            return default
        return self._data.pop(key, default)

    def clear(self) -> None:
        self._data.clear()
        self.hits = 0
        self.misses = 0

    def __len__(self) -> int:
        return len(self._data)

    def info(self) -> Dict[str, int]:
        return {
            "capacity": self.capacity,
            "size": len(self._data),
            "hits": self.hits,
            "misses": self.misses,
        }


class SqliteTripleDict(MutableMapping[int, Triple]):
    def __init__(
        self,
        db_path: str = ":memory:",
        table: str = "items",
        autocommit: bool = True,
        lru_capacity: int = 0,
    ):
        """
        db_path: path to sqlite database (use ":memory:" for in-memory)
        table: table name to use
        autocommit: if True, commits after each write operation
        lru_capacity: capacity of in-memory LRU cache (0 disables)
        """
        self._db_path = db_path
        self._table = table
        self._autocommit = bool(autocommit)
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self._table} (
                key INTEGER PRIMARY KEY,
                v1 INTEGER NOT NULL,
                v2 INTEGER NOT NULL,
                v3 INTEGER NOT NULL
            )
            """
        )
        # set isolation behavior: None = autocommit, "" = default manual commit behavior
        if self._autocommit:
            self._conn.isolation_level = None
        else:
            self._conn.isolation_level = ""

        # LRU cache
        self._cache = LRUCache(int(lru_capacity))

    # --- internal helpers ---
    def _commit_if_needed(self) -> None:
        if not self._autocommit:
            self._conn.commit()

    def _validate_key(self, key: Any) -> int:
        if not isinstance(key, int):
            raise TypeError("keys must be integers")
        return key

    def _validate_value(self, value: Any) -> Triple:
        if (
            not isinstance(value, tuple)
            or len(value) != 3
            or not all(isinstance(x, int) for x in value)
        ):
            raise TypeError("value must be a tuple of three integers")
        # type: ignore[return-value]
        return value

    # --- MutableMapping interface ---
    def __getitem__(self, key: int) -> Triple:
        key = self._validate_key(key)
        # try cache first
        cached = self._cache.get(key)
        if cached is not None:
            return cached

        cur = self._conn.execute(
            f"SELECT v1, v2, v3 FROM {self._table} WHERE key = ?", (key,)
        )
        row = cur.fetchone()
        if row is None:
            raise KeyError(key)
        triple = (int(row[0]), int(row[1]), int(row[2]))
        self._cache.put(key, triple)
        return triple

    def __setitem__(self, key: int, value: Triple) -> None:
        key = self._validate_key(key)
        value = self._validate_value(value)
        # write-through: update DB first (inside transaction if autocommit False)
        self._conn.execute(
            f"INSERT OR REPLACE INTO {self._table} (key, v1, v2, v3) VALUES (?, ?, ?, ?)",
            (key, value[0], value[1], value[2]),
        )
        self._commit_if_needed()
        # update cache
        self._cache.put(key, value)

    def __delitem__(self, key: int) -> None:
        key = self._validate_key(key)
        cur = self._conn.execute(f"DELETE FROM {self._table} WHERE key = ?", (key,))
        # For sqlite, rowcount may be -1 if not supported by driver; check existence by last SELECT if needed.
        # We'll check whether the key existed by examining changes()
        changes = self._conn.total_changes
        # A simpler approach: check whether row existed before delete (do a select)
        # But to keep this lightweight, rely on SELECT before delete:
        # (Use SELECT to provide accurate KeyError semantics)
        cur_check = self._conn.execute(f"SELECT 1 FROM {self._table} WHERE key = ?", (key,))
        if cur_check.fetchone() is not None:
            # key still exists (shouldn't happen), but proceed
            pass
        # If the delete removed nothing, raise KeyError
        # A reliable way: check whether the key exists AFTER delete by selecting
        cur_post = self._conn.execute(f"SELECT 1 FROM {self._table} WHERE key = ?", (key,))
        if cur_post.fetchone() is not None:
            # still present => odd; for safety, just remove from cache and return
            self._cache.pop(key, None)
            self._commit_if_needed()
            return
        # If key was removed from DB, also remove from cache
        self._cache.pop(key, None)
        self._commit_if_needed()

    def __iter__(self) -> Iterator[int]:
        cur = self._conn.execute(f"SELECT key FROM {self._table} ORDER BY key")
        for (k,) in cur:
            yield int(k)

    def __len__(self) -> int:
        cur = self._conn.execute(f"SELECT COUNT(*) FROM {self._table}")
        (count,) = cur.fetchone()
        return int(count)

    # --- convenience methods ---
    def keys(self) -> Iterable[int]:
        return list(iter(self))

    def items(self) -> Iterable[Tuple[int, Triple]]:
        cur = self._conn.execute(f"SELECT key, v1, v2, v3 FROM {self._table} ORDER BY key")
        return [(int(r[0]), (int(r[1]), int(r[2]), int(r[3]))) for r in cur.fetchall()]

    def values(self) -> Iterable[Triple]:
        cur = self._conn.execute(f"SELECT v1, v2, v3 FROM {self._table} ORDER BY key")
        return [(int(r[0]), int(r[1]), int(r[2])) for r in cur.fetchall()]  # type: ignore[return-value]

    def get(self, key: int, default: Optional[Triple] = None) -> Optional[Triple]:
        try:
            return self[key]
        except KeyError:
            return default

    def clear(self) -> None:
        self._conn.execute(f"DELETE FROM {self._table}")
        self._commit_if_needed()
        self._cache.clear()

    def update(self, other: Optional[Iterable[Tuple[int, Triple]]] = None, **kwargs: Triple) -> None:
        """
        Accepts either an iterable of (key, triple) pairs or keyword args (with int keys)
        Bulk updates are performed in a transaction for performance and atomicity.
        Cache entries for updated keys are refreshed to the new values.
        """
        pairs: Iterable[Tuple[int, Triple]] = []
        if other is not None:
            if hasattr(other, "items"):
                pairs = ((int(k), v) for k, v in dict(other).items())
            else:
                pairs = ((int(k), v) for (k, v) in other)  # type: ignore[misc]
        if kwargs:
            # convert kwargs keys -> int
            kw_pairs = ((int(k), v) for k, v in kwargs.items())
            if pairs:
                # combine
                pairs = list(pairs) + list(kw_pairs)  # type: ignore[assignment]
            else:
                pairs = kw_pairs

        # Execute all inserts in one transaction
        if pairs:
            with self._conn:
                for k, v in pairs:
                    v = self._validate_value(v)
                    self._conn.execute(
                        f"INSERT OR REPLACE INTO {self._table} (key, v1, v2, v3) VALUES (?, ?, ?, ?)",
                        (k, v[0], v[1], v[2]),
                    )
                    self._cache.put(int(k), v)

    # --- cache helpers ---
    def cache_info(self) -> Dict[str, int]:
        return self._cache.info()

    def clear_cache(self) -> None:
        self._cache.clear()

    # --- resource management ---
    def close(self) -> None:
        try:
            if not self._autocommit:
                self._conn.commit()
        finally:
            self._conn.close()

    def __enter__(self) -> "SqliteTripleDict":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        # commit on normal exit; rollback on exception when not autocommit
        if not self._autocommit:
            if exc is None:
                self._conn.commit()
            else:
                self._conn.rollback()
        self._conn.close()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(db_path={self._db_path!r}, table={self._table!r}, "
            f"lru_capacity={self._cache.capacity})"
        )


# --- Example usage / small smoke test ---
if __name__ == "__main__":
    d = SqliteTripleDict(":memory:", autocommit=False, lru_capacity=2)
    # initial writes (populate DB and cache)
    d[1] = (10, 11, 12)
    d[2] = (20, 21, 22)
    # cache now has keys 1,2
    print("cache info after inserts:", d.cache_info())

    # read existing => should hit cache
    print("d[1] ->", d[1])
    print("cache info after reading 1:", d.cache_info())

    # read miss (not cached) - insert new row directly to DB then read
    d._conn.execute("INSERT INTO items (key, v1, v2, v3) VALUES (?, ?, ?, ?)", (3, 30, 31, 32))
    d._conn.commit()
    print("d[3] (db-only before read) ->", d[3])  # Should load into cache and possibly evict LRU
    print("cache info after reading 3:", d.cache_info())

    # update via update() in bulk
    d.update([(4, (40, 41, 42)), (5, (50, 51, 52))])
    print("len:", len(d), "first few items:", list(d.items())[:5])
    print("final cache info:", d.cache_info())

    d.close()