import sqlite3
import os
import typing


class BlobDict:
    """
    Simple dict-like mapping: fixed-length BLOB key -> BLOB value, backed by SQLite.

    - key_size: number of bytes each key must have (enforced by a CHECK in the table and by the API).
    - Uses a WITHOUT ROWID table so the BLOB primary key is stored as the table key.
    """

    def __init__(self, path=":memory:", table="kv", key_size=16, pragmas=None):
        if not isinstance(key_size, int) or key_size <= 0:
            raise ValueError("key_size must be a positive integer")
        if not isinstance(table, str) or not table:
            raise ValueError("table name must be a non-empty string")
        # Basic validation for the table name (prevents obvious SQL injection)
        if not all(c.isalnum() or c == "_" for c in table):
            raise ValueError("table name may contain only alphanumeric characters and underscores")

        self.path = path
        self.table = table
        self.key_size = key_size
        self._conn = sqlite3.connect(self.path)
        # Ensure sqlite returns bytes for BLOB columns (default behavior)
        # Apply common pragmas if provided
        if pragmas:
            cur = self._conn.cursor()
            for p, v in pragmas.items():
                cur.execute(f"PRAGMA {p} = {v}")
            cur.close()

        # Create table with CHECK(length(key) = key_size)
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS "{self.table}" (
            key   BLOB PRIMARY KEY,
            value BLOB,
            CHECK(length(key) = {self.key_size})
        ) WITHOUT ROWID;
        """
        self._conn.execute(create_sql)
        self._conn.commit()

    def close(self):
        if self._conn:
            try:
                self._conn.commit()
            except Exception:
                pass
            self._conn.close()
            self._conn = None

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    # Basic mapping protocol
    def __setitem__(self, key, value):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes or bytearray")
        if len(key) != self.key_size:
            raise ValueError(f"key must be exactly {self.key_size} bytes")
        # Normalize bytearray to bytes
        if isinstance(key, bytearray):
            key = bytes(key)
        if isinstance(value, bytearray):
            value = bytes(value)

        sql = f'INSERT INTO "{self.table}"(key, value) VALUES(?,?) ' \
              f'ON CONFLICT(key) DO UPDATE SET value=excluded.value'
        self._conn.execute(sql, (key, value))
        self._conn.commit()

    def __getitem__(self, key):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes or bytearray")
        if len(key) != self.key_size:
            raise KeyError("key of incorrect length")
        row = self._conn.execute(f'SELECT value FROM "{self.table}" WHERE key = ?', (bytes(key),)).fetchone()
        if row is None:
            raise KeyError(key)
        return row[0]

    def __delitem__(self, key):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key must be bytes or bytearray")
        if len(key) != self.key_size:
            raise KeyError("key of incorrect length")
        cur = self._conn.execute(f'DELETE FROM "{self.table}" WHERE key = ?', (bytes(key),))
        self._conn.commit()
        if cur.rowcount == 0:
            raise KeyError(key)

    def __contains__(self, key):
        if not isinstance(key, (bytes, bytearray)):
            return False
        if len(key) != self.key_size:
            return False
        row = self._conn.execute(f'SELECT 1 FROM "{self.table}" WHERE key = ? LIMIT 1', (bytes(key),)).fetchone()
        return row is not None

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        cur = self._conn.execute(f'SELECT key FROM "{self.table}"')
        for (k,) in cur:
            yield k

    def values(self):
        cur = self._conn.execute(f'SELECT value FROM "{self.table}"')
        for (v,) in cur:
            yield v

    def items(self):
        cur = self._conn.execute(f'SELECT key, value FROM "{self.table}"')
        for k, v in cur:
            yield k, v

    def __iter__(self):
        return self.keys()

    def __len__(self):
        cur = self._conn.execute(f'SELECT COUNT(*) FROM "{self.table}"')
        return cur.fetchone()[0]

    def clear(self):
        self._conn.execute(f'DELETE FROM "{self.table}"')
        self._conn.commit()

    # Optional helper: atomic bulk put (transaction)
    def update_many(self, pairs: typing.Iterable[typing.Tuple[bytes, bytes]]):
        cur = self._conn.cursor()
        sql = f'INSERT INTO "{self.table}"(key, value) VALUES(?,?) ' \
              f'ON CONFLICT(key) DO UPDATE SET value=excluded.value'
        for k, v in pairs:
            if not isinstance(k, (bytes, bytearray)) or len(k) != self.key_size:
                raise ValueError("all keys must be bytes of the configured fixed length")
            if isinstance(k, bytearray):
                k = bytes(k)
            if isinstance(v, bytearray):
                v = bytes(v)
            cur.execute(sql, (k, v))
        self._conn.commit()