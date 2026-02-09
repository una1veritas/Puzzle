import sqlite3
from typing import List, Tuple, Iterator, Union

class Int64PairStorage:
    """
    A class to manage storage of 64-bit integer pairs in SQLite database.
    Implements set-like interface for convenient usage.
    """
    
    def __init__(self, db_path: str = 'pairs.db'):
        """Initialize database connection and create table if needed."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()
    
    def _create_table(self) -> None:
        """Create the pairs table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value1 INTEGER NOT NULL,
                value2 INTEGER NOT NULL,
                UNIQUE(value1, value2)
            )
        ''')
        self.conn.commit()
    
    def add(self, value1: int, value2: int) -> None:
        """
        Add a pair of 64-bit integers to the storage (set-like behavior).
        Duplicates are automatically ignored due to UNIQUE constraint.
        
        Args:
            value1: First 64-bit integer
            value2: Second 64-bit integer
        """
        try:
            self.cursor.execute(
                'INSERT INTO pairs (value1, value2) VALUES (?, ?)',
                (value1, value2)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Pair already exists, ignore (set behavior)
            pass
    
    def discard(self, value1: int, value2: int) -> None:
        """
        Remove a pair from storage if it exists (set-like behavior).
        Does not raise error if pair doesn't exist.
        
        Args:
            value1: First 64-bit integer
            value2: Second 64-bit integer
        """
        self.cursor.execute(
            'DELETE FROM pairs WHERE value1 = ? AND value2 = ?',
            (value1, value2)
        )
        self.conn.commit()
    
    def remove(self, value1: int, value2: int) -> None:
        """
        Remove a pair from storage. Raises KeyError if pair doesn't exist.
        
        Args:
            value1: First 64-bit integer
            value2: Second 64-bit integer
            
        Raises:
            KeyError: If pair is not found in storage
        """
        self.cursor.execute(
            'DELETE FROM pairs WHERE value1 = ? AND value2 = ?',
            (value1, value2)
        )
        self.conn.commit()
        if self.cursor.rowcount == 0:
            raise KeyError(f"Pair ({value1}, {value2}) not found in storage")
    
    def __contains__(self, pair: Tuple[int, int]) -> bool:
        """
        Check if a pair exists in storage (enables 'in' operator).
        
        Args:
            pair: Tuple of (value1, value2)
            
        Returns:
            True if pair exists, False otherwise
        """
        value1, value2 = pair
        self.cursor.execute(
            'SELECT 1 FROM pairs WHERE value1 = ? AND value2 = ? LIMIT 1',
            (value1, value2)
        )
        return self.cursor.fetchone() is not None
    
    def __iter__(self) -> Iterator[Tuple[int, int]]:
        """
        Iterate over all pairs in storage (enables 'for' loops).
        
        Yields:
            Tuples of (value1, value2)
        """
        self.cursor.execute('SELECT value1, value2 FROM pairs')
        for row in self.cursor.fetchall():
            yield row
    
    def __len__(self) -> int:
        """
        Get the number of pairs in storage (enables len() function).
        
        Returns:
            Number of pairs
        """
        self.cursor.execute('SELECT COUNT(*) FROM pairs')
        return self.cursor.fetchone()[0]
    
    def __bool__(self) -> bool:
        """
        Check if storage is non-empty (enables boolean context).
        
        Returns:
            True if storage has at least one pair, False otherwise
        """
        return len(self) > 0
    
    def __repr__(self) -> str:
        """
        String representation of storage.
        
        Returns:
            String showing all pairs
        """
        pairs = list(self)
        return f"Int64PairStorage({set(pairs)})"
    
    def __eq__(self, other) -> bool:
        """
        Compare two storages for equality.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            True if both contain the same pairs
        """
        if not isinstance(other, Int64PairStorage):
            return False
        return set(self) == set(other)
    
    # Set-like operations
    
    def union(self, other: 'Int64PairStorage') -> 'Int64PairStorage':
        """
        Create a new storage containing pairs from both storages.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            New Int64PairStorage with combined pairs
        """
        result = Int64PairStorage(':memory:')
        for pair in self:
            result.add(*pair)
        for pair in other:
            result.add(*pair)
        return result
    
    def intersection(self, other: 'Int64PairStorage') -> 'Int64PairStorage':
        """
        Create a new storage containing only pairs present in both storages.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            New Int64PairStorage with common pairs
        """
        result = Int64PairStorage(':memory:')
        for pair in self:
            if pair in other:
                result.add(*pair)
        return result
    
    def difference(self, other: 'Int64PairStorage') -> 'Int64PairStorage':
        """
        Create a new storage with pairs in this storage but not in other.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            New Int64PairStorage with difference
        """
        result = Int64PairStorage(':memory:')
        for pair in self:
            if pair not in other:
                result.add(*pair)
        return result
    
    def issubset(self, other: 'Int64PairStorage') -> bool:
        """
        Check if all pairs in this storage are in another storage.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            True if this is a subset of other
        """
        return set(self).issubset(set(other))
    
    def issuperset(self, other: 'Int64PairStorage') -> bool:
        """
        Check if this storage contains all pairs from another storage.
        
        Args:
            other: Another Int64PairStorage object
            
        Returns:
            True if this is a superset of other
        """
        return set(self).issuperset(set(other))
    
    def clear(self) -> None:
        """Clear all pairs from storage."""
        self.cursor.execute('DELETE FROM pairs')
        self.conn.commit()
    
    def copy(self) -> 'Int64PairStorage':
        """
        Create a copy of this storage in a new database.
        
        Returns:
            New Int64PairStorage with same pairs
        """
        result = Int64PairStorage(':memory:')
        for pair in self:
            result.add(*pair)
        return result
    
    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()

    # Context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example usage
if __name__ == '__main__':
    print("=== SQLite Pair Storage - Set-like Interface ===\n")
    
    # Create storages
    storage1 = Int64PairStorage('pairs1.db')
    storage2 = Int64PairStorage('pairs2.db')
    
    # Clear previous data
    storage1.clear()
    storage2.clear()
    
    # Add pairs using add() method
    print("Adding pairs to storage1...")
    storage1.add(100, 200)
    storage1.add(300, 400)
    storage1.add(500, 600)
    storage1.add(700, 800)
    print(f"Storage1: {storage1}")
    
    print("\nAdding pairs to storage2...")
    storage2.add(300, 400)
    storage2.add(500, 600)
    storage2.add(900, 1000)
    print(f"Storage2: {storage2}")
    
    # Test 'in' operator
    print("\n--- Testing 'in' operator ---")
    print(f"(100, 200) in storage1: {(100, 200) in storage1}")
    print(f"(100, 200) in storage2: {(100, 200) in storage2}")
    print(f"(300, 400) in storage2: {(300, 400) in storage2}")
    
    # Test len()
    print("\n--- Testing len() ---")
    print(f"len(storage1): {len(storage1)}")
    print(f"len(storage2): {len(storage2)}")
    
    # Test iteration
    print("\n--- Testing iteration ---")
    print("Pairs in storage1:")
    for pair in storage1:
        print(f"  {pair}")
    
    # Test discard (no error if not found)
    print("\n--- Testing discard() ---")
    storage1.discard(100, 200)
    print(f"After discarding (100, 200): {storage1}")
    storage1.discard(999, 999)  # Doesn't exist, no error
    print("Discarded non-existent pair (999, 999) - no error")
    
    # Test remove (raises KeyError if not found)
    print("\n--- Testing remove() ---")
    try:
        storage1.remove(999, 999)
    except KeyError as e:
        print(f"remove() raised KeyError: {e}")
    
    # Test set operations
    print("\n--- Testing set operations ---")
    print(f"Union: {storage1.union(storage2)}")
    print(f"Intersection: {storage1.intersection(storage2)}")
    print(f"Difference (storage1 - storage2): {storage1.difference(storage2)}")
    
    # Test subset/superset
    print("\n--- Testing subset/superset ---")
    print(f"storage2.issubset(storage1): {storage2.issubset(storage1)}")
    print(f"storage1.issuperset(storage2): {storage1.issuperset(storage2)}")
    
    # Test copy
    print("\n--- Testing copy() ---")
    storage3 = storage1.copy()
    print(f"Copy of storage1: {storage3}")
    
    # Test equality
    print("\n--- Testing equality ---")
    print(f"storage1 == storage3: {storage1 == storage3}")
    print(f"storage1 == storage2: {storage1 == storage2}")
    
    # Test boolean context
    print("\n--- Testing boolean context ---")
    print(f"bool(storage1): {bool(storage1)}")
    storage_empty = Int64PairStorage(':memory:')
    print(f"bool(empty storage): {bool(storage_empty)}")
    
    # Test duplicate prevention
    print("\n--- Testing duplicate prevention ---")
    storage_test = Int64PairStorage(':memory:')
    storage_test.add(111, 222)
    print(f"Added (111, 222), length: {len(storage_test)}")
    storage_test.add(111, 222)  # Try to add duplicate
    print(f"Added (111, 222) again, length: {len(storage_test)} (unchanged)")
    
    # Cleanup
    storage1.close()
    storage2.close()
    storage3.close()
    storage_empty.close()
    storage_test.close()
    print("\nDatabase connections closed.")