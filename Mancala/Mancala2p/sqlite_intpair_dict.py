import sqlite3
from typing import Any, Iterator, Tuple


class SQLiteDict:
    """
    A dictionary-like class that maps pairs of integers (as keys) to integer values,
    storing data in an SQLite database.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        """
        Initialize the SQLiteDict.
        
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
            CREATE TABLE IF NOT EXISTS kv_store (
                key1 INTEGER NOT NULL,
                key2 INTEGER NOT NULL,
                value INTEGER NOT NULL,
                PRIMARY KEY (key1, key2)
            )
        """)
        self.connection.commit()
    
    def __setitem__(self, key: Tuple[int, int], value: int) -> None:
        """
        Set a value for a key pair (key1, key2).
        
        Args:
            key: A tuple of two integers (key1, key2)
            value: The integer value to store
            
        Raises:
            TypeError: If key is not a tuple of two integers or value is not an integer
        """
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Key must be a tuple of two integers")
        if not all(isinstance(k, int) for k in key):
            raise TypeError("Both elements of key must be integers")
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        
        key1, key2 = key
        self.cursor.execute(
            "INSERT OR REPLACE INTO kv_store (key1, key2, value) VALUES (?, ?, ?)",
            (key1, key2, value)
        )
        self.connection.commit()
    
    def __getitem__(self, key: Tuple[int, int]) -> int:
        """
        Get a value for a key pair (key1, key2).
        
        Args:
            key: A tuple of two integers (key1, key2)
            
        Returns:
            The integer value associated with the key pair
            
        Raises:
            KeyError: If the key pair doesn't exist
            TypeError: If key is not a tuple of two integers
        """
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Key must be a tuple of two integers")
        
        key1, key2 = key
        self.cursor.execute(
            "SELECT value FROM kv_store WHERE key1 = ? AND key2 = ?",
            (key1, key2)
        )
        result = self.cursor.fetchone()
        
        if result is None:
            raise KeyError(key)
        return result[0]
    
    def __delitem__(self, key: Tuple[int, int]) -> None:
        """
        Delete a key pair from the database.
        
        Args:
            key: A tuple of two integers (key1, key2)
            
        Raises:
            KeyError: If the key pair doesn't exist
            TypeError: If key is not a tuple of two integers
        """
        if not isinstance(key, tuple) or len(key) != 2:
            raise TypeError("Key must be a tuple of two integers")
        
        key1, key2 = key
        self.cursor.execute(
            "DELETE FROM kv_store WHERE key1 = ? AND key2 = ?",
            (key1, key2)
        )
        self.connection.commit()
        
        if self.cursor.rowcount == 0:
            raise KeyError(key)
    
    def __contains__(self, key: Tuple[int, int]) -> bool:
        """
        Check if a key pair exists in the database.
        
        Args:
            key: A tuple of two integers (key1, key2)
            
        Returns:
            True if the key pair exists, False otherwise
        """
        if not isinstance(key, tuple) or len(key) != 2:
            return False
        
        key1, key2 = key
        self.cursor.execute(
            "SELECT 1 FROM kv_store WHERE key1 = ? AND key2 = ? LIMIT 1",
            (key1, key2)
        )
        return self.cursor.fetchone() is not None
    
    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the database.
        
        Returns:
            The count of key-value pairs
        """
        self.cursor.execute("SELECT COUNT(*) FROM kv_store")
        return self.cursor.fetchone()[0]
    
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        """
        Iterate over all key pairs in the database.
        
        Yields:
            Tuples of (key1, key2)
        """
        self.cursor.execute("SELECT key1, key2 FROM kv_store")
        for row in self.cursor.fetchall():
            yield tuple(row)
    
    def __repr__(self) -> str:
        """Get a string representation of the SQLiteDict."""
        items = {key: self[key] for key in self}
        return f"SQLiteDict({items})"
    
    def keys(self) -> Iterator[Tuple[int, int]]:
        """
        Get an iterator over all key pairs.
        
        Returns:
            Iterator of (key1, key2) tuples
        """
        return iter(self)
    
    def values(self) -> Iterator[int]:
        """
        Get an iterator over all values.
        
        Yields:
            Integer values
        """
        self.cursor.execute("SELECT value FROM kv_store")
        for row in self.cursor.fetchall():
            yield row[0]
    
    def items(self) -> Iterator[Tuple[Tuple[int, int], int]]:
        """
        Get an iterator over all (key, value) pairs.
        
        Yields:
            Tuples of ((key1, key2), value)
        """
        self.cursor.execute("SELECT key1, key2, value FROM kv_store")
        for row in self.cursor.fetchall():
            yield ((row[0], row[1]), row[2])
    
    def get(self, key: Tuple[int, int], default: Any = None) -> Any:
        """
        Get a value for a key pair with a default fallback.
        
        Args:
            key: A tuple of two integers (key1, key2)
            default: Value to return if key doesn't exist
            
        Returns:
            The value associated with the key pair, or default
        """
        try:
            return self[key]
        except (KeyError, TypeError):
            return default
    
    def pop(self, key: Tuple[int, int], *args) -> int:
        """
        Remove and return the value for a key pair.
        
        Args:
            key: A tuple of two integers (key1, key2)
            *args: Optional default value if key doesn't exist
            
        Returns:
            The value that was associated with the key pair
            
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
        self.cursor.execute("DELETE FROM kv_store")
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
    d = SQLiteDict()
    
    # Set values
    d[(1, 2)] = 100
    d[(3, 4)] = 200
    d[(5, 6)] = 300
    
    # Get values
    print(f"d[(1, 2)] = {d[(1, 2)]}")  # Output: 100
    
    # Check membership
    print(f"(1, 2) in d: {(1, 2) in d}")  # Output: True
    print(f"(99, 99) in d: {(99, 99) in d}")  # Output: False
    
    # Get length
    print(f"len(d) = {len(d)}")  # Output: 3
    
    # Iterate
    print("All items:")
    for key, value in d.items():
        print(f"  {key}: {value}")
    
    # Delete item
    del d[(3, 4)]
    print(f"After deleting (3, 4), len(d) = {len(d)}")  # Output: 2
    
    # Use context manager
    with SQLiteDict("example.db") as db:
        db[(10, 20)] = 1000
        print(f"db[(10, 20)] = {db[(10, 20)]}")
    
    # Clean up
    d.close()