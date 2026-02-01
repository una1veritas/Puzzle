from __future__ import annotations
'''
Created on 2026/01/31

@author: sin
'''

#!/usr/bin/env python3
"""
Sqlite-backed dict-like mapping: int -> (int, int, int)

Implements collections.abc.MutableMapping so it behaves like a normal dict.
"""


import sqlite3
from collections.abc import MutableMapping, Iterator
from typing import Dict, Iterable, Tuple, Optional, Any


Triple = Tuple[int, int, int]


class SqliteTripleDict(MutableMapping[int, Triple]):
    def __init__(self, db_path: str = ":memory:", table: str = "items", autocommit: bool = True):
        """
        db_path: path to sqlite database (use ":memory:" for in-memory)
        table: table name to use
        autocommit: if True, commits after each write operation
        """
        self._db_path = db_path
        self._table = table
        self._autocommit = autocommit
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
        if self._autocommit:
            self._conn.isolation_level = None  # autocommit mode
        else:
            self._conn.isolation_level = ""  # default (manual commit)

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
        return value  # type: ignore[return-value]

    # --- MutableMapping interface ---
    def __getitem__(self, key: int) -> Triple:
        key = self._validate_key(key)
        cur = self._conn.execute(
            f"SELECT v1, v2, v3 FROM {self._table} WHERE key = ?", (key,)
        )
        row = cur.fetchone()
        if row is None:
            raise KeyError(key)
        return (int(row[0]), int(row[1]), int(row[2]))

    def __setitem__(self, key: int, value: Triple) -> None:
        key = self._validate_key(key)
        value = self._validate_value(value)
        self._conn.execute(
            f"INSERT OR REPLACE INTO {self._table} (key, v1, v2, v3) VALUES (?, ?, ?, ?)",
            (key, value[0], value[1], value[2]),
        )
        self._commit_if_needed()

    def __delitem__(self, key: int) -> None:
        key = self._validate_key(key)
        cur = self._conn.execute(f"DELETE FROM {self._table} WHERE key = ?", (key,))
        if cur.rowcount == 0:
            raise KeyError(key)
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

    def update(self, other: Optional[Iterable[Tuple[int, Triple]]] = None, **kwargs: Triple) -> None:
        """
        Accepts either an iterable of (key, triple) pairs or keyword args (with int keys)
        Example: d.update([(1, (1,2,3)), (2, (4,5,6))]) or d.update(**{ "3": (7,8,9) })
        Note: kwargs keys will be converted to int(), so provide numeric keys as strings only if safe.
        """
        if other is not None:
            # other might be mapping or iterable of pairs
            if hasattr(other, "items"):
                iterator = ((int(k), v) for k, v in cast(Dict[int, Triple], other).items())
            else:
                iterator = other  # type: ignore[assignment]
            with self._conn:
                for k, v in iterator:
                    k = int(k)
                    v = self._validate_value(v)
                    self._conn.execute(
                        f"INSERT OR REPLACE INTO {self._table} (key, v1, v2, v3) VALUES (?, ?, ?, ?)",
                        (k, v[0], v[1], v[2]),
                    )
                # if autocommit is False, with-block commits at end; if autocommit True, sqlite autocommits
        if kwargs:
            # convert kwargs keys -> int
            for k, v in kwargs.items():
                self[int(k)] = v

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
        return f"{self.__class__.__name__}(db_path={self._db_path!r}, table={self._table!r})"

if __name__ == "__main__":
    d = SqliteTripleDict("data.db", autocommit=False)  # persistent DB, manual commit
    d[1] = (10, 20, 30)
    d[2] = (100, 200, 300)
    print(len(d))           # 2
    print(d[1])             # (10, 20, 30)
    print(list(d.items()))  # [(1, (10,20,30)), (2, (100,200,300))]
    del d[1]
    print(d.get(1, None))   # None
    d.close()
