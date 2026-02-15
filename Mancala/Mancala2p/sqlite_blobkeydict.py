import sqlite3
from typing import Any, Iterator, Tuple


class SQLiteBlobDict:
    """
    A dictionary-like class that maps pairs of integers (as keys) to integer values,
    storing data in an SQLite database.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the SQLiteBlobDict.
        
        Args:
            db_path: Path to the SQLite database file. 
                    Default is ":memory:" for in-memory database.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_table()
    
    def _create_table(self) -> None:
        """Create the key-value storage table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blob_dict (
                key BLOB NOT NULL PRIMARY KEY,
                value INTEGER NOT NULL
            )
        """)
        self.connection.commit()
    
    def __setitem__(self, key: bytes, value: int) -> None:
        """
        Set a value for a key (key1, key2).
        """
        if not isinstance(key, bytes) :
            raise TypeError("Key must be a bytes-sequence")
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        
        self.cursor.execute(
            "INSERT OR REPLACE INTO blob_dict (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.connection.commit()
    
    def __getitem__(self, key: bytes) -> int:
        """
        Get a value for a key (bytes).
        """
        if not isinstance(key, bytes) :
            raise TypeError("Key must be a bytes-sequence")
        
        self.cursor.execute(
            "SELECT value FROM blob_dict WHERE key = ?",
            (key, )
        )
        result = self.cursor.fetchone()
        
        if result is None:
            raise KeyError(key)
        return result[0]
    
    def __delitem__(self, key: bytes) -> None:
        """
        Delete a key from the database.

        """
        if not isinstance(key, bytes):
            raise TypeError("Key must be a bytes sequence")
        
        self.cursor.execute(
            "DELETE FROM blob_dict WHERE key = ?",
            (key, )
        )
        self.connection.commit()
        
        if self.cursor.rowcount == 0:
            raise KeyError(key)
    
    def __contains__(self, key: bytes) -> bool:
        """
        Check if a key pair exists in the database.
        """
        if not isinstance(key, bytes) :
            return False
        
        self.cursor.execute(
            "SELECT 1 FROM blob_dict WHERE key = ? LIMIT 1",
            (key, )
        )
        return self.cursor.fetchone() is not None
    
    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the database.
        
        Returns:
            The count of key-value pairs
        """
        self.cursor.execute("SELECT COUNT(*) FROM blob_dict")
        return self.cursor.fetchone()[0]
    
    def __iter__(self) -> Iterator[Tuple[bytes]]:
        """
        Iterate over all keys in the database.
        """
        self.cursor.execute("SELECT key FROM blob_dict")
        for row in self.cursor.fetchall():
            yield tuple(row)
    
    def __repr__(self) -> str:
        """Get a string representation of the SQLiteBlobDict."""
        items = {key: self[key] for key in self}
        return f"SQLiteBlobDict({items})"
    
    def keys(self) -> Iterator[bytes]:
        """
        Get an iterator over all keys.
        
        Returns:
            Iterator of key
        """
        return iter(self)
    
    def values(self) -> Iterator[int]:
        """
        Get an iterator over all values.
        
        Yields:
            Integer values
        """
        self.cursor.execute("SELECT value FROM blob_dict")
        for row in self.cursor.fetchall():
            yield row[0]
    
    def items(self) -> Iterator[Tuple[bytes, int]]:
        """
        Get an iterator over all (key, value) pairs.
        
        Yields:
            Tuples of (key, value)
        """
        self.cursor.execute("SELECT key, value FROM blob_dict")
        for row in self.cursor.fetchall():
            yield (row[0], row[1])
    
    def get(self, key: bytes, default: Any = None) -> Any:
        """
        Get a value for a key with a default fallback.
    
        returns the value associated with the key, or default
        """
        try:
            return self[key]
        except (KeyError, TypeError):
            return default
    
    def pop(self, key: bytes, *args) -> int:
        """
        Remove and return the value for a key.

        Raises:
            KeyError: If key doesn't exist and no default is provided
        """
        if len(args) > 1:
            raise TypeError(f"pop expected at most 2 arguments, got {len(args) + 1}")
        
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if args:
                return args[0]
            raise
    
    def clear(self) -> None:
        """Delete all key-value pairs from the database."""
        self.cursor.execute("DELETE FROM blob_dict")
        self.connection.commit()
    
    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage
if __name__ == "__main__":
    # Create an in-memory database
    d = SQLiteBlobDict()
    
    # Set values
    d[bytes((1, 2))] = 100
    d[bytes((3, 4))] = 200
    d[bytes((5, 6))] = 300
    
    # Get values
    k= bytes( (1, 2) )
    print(f"d[{k}] = {d[k]}")  # Output: 100
    
    # Check membership
    print(f"bytes((5, 6)) in d: {bytes((5, 6)) in d}")  # Output: True
    print(f"bytes(99, 99) in d: {bytes((99, 99)) in d}")  # Output: False
    
    # Get length
    print(f"len(d) = {len(d)}")  # Output: 3
    
    # Iterate
    print("All items:")
    for key, value in d.items():
        print(f"  {key}: {value}")
    
    # Delete item
    del d[bytes((3, 4))]
    print(f"After deleting (3, 4), len(d) = {len(d)}")  # Output: 2
    
    # Use context manager
    with SQLiteBlobDict("example.db") as db:
        db[bytes((10, 20))] = 1000
        print(f"db[bytes((10, 20))] = {db[bytes((10, 20))]}")
    
    # Clean up
    d.close()
    