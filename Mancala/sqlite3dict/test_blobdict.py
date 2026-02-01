import os
from blobdict import BlobDict

DB_FILE = "test_kv.db"


def main():
    # Remove previous test DB if any
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # Create a BlobDict with 16-byte keys
    with BlobDict(DB_FILE, table="kv", key_size=16) as d:
        k1 = b"\x00" * 16
        v1 = b"hello blob 1"
        k2 = bytes(range(16))  # 16 bytes: 0..15
        v2 = b"\x01\x02\x03"

        # Insert two pairs
        d[k1] = v1
        d[k2] = v2

        # Read back
        print("d[k1] ->", d[k1])
        print("d[k2] ->", d[k2])

        # Update value
        d[k1] = b"updated"
        print("after update d[k1] ->", d[k1])

        # Contains and length
        print("k1 in d?", k1 in d)
        print("len(d) =", len(d))

        # Iterate keys and items
        print("keys:")
        for key in d.keys():
            print(" ", key)
        print("items:")
        for key, val in d.items():
            print(" ", key, "->", val)

        # Delete k2
        del d[k2]
        print("after delete, k2 in d?", k2 in d)
        print("len(d) =", len(d))

        # Clear all
        d.clear()
        print("after clear, len(d) =", len(d))

    # Clean up test DB file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)


if __name__ == "__main__":
    main()