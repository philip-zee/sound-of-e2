from collections import OrderedDict
import time

class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.cache = OrderedDict()   # key → (value, timestamp)

    def _update_timestamp(self, key):
        """Refresh timestamp and move key to the end (most recently used)."""
        value, _ = self.cache[key]
        timestamp = time.time()
        self.cache[key] = (value, timestamp)
        self.cache.move_to_end(key)  # mark as recently used

    def get(self, key):
        """Return value and update LRU timestamp. Returns None if not present."""
        if key not in self.cache:
            return None
        self._update_timestamp(key)
        return self.cache[key][0]

    def put(self, key, value):
        """Insert or update an entry and refresh timestamp."""
        timestamp = time.time()

        if key in self.cache:
            # update value and refresh position
            self.cache[key] = (value, timestamp)
            self.cache.move_to_end(key)
        else:
            # evict oldest if full
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)  # remove LRU
            self.cache[key] = (value, timestamp)

    def __contains__(self, key):
        return key in self.cache

    def __len__(self):
        return len(self.cache)

    def __repr__(self):
        return f"LRUCache({self.cache})"
