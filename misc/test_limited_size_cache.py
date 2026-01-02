import pytest
import time
from limited_size_cache import LRUCache


class TestLRUCacheInitialization:
    """Test cases for LRUCache initialization."""

    def test_init_valid_capacity(self):
        """Test creating LRUCache with valid capacity."""
        cache = LRUCache(5)
        assert cache.capacity == 5
        assert len(cache) == 0

    def test_init_capacity_one(self):
        """Test creating LRUCache with capacity of 1."""
        cache = LRUCache(1)
        assert cache.capacity == 1

    def test_init_large_capacity(self):
        """Test creating LRUCache with large capacity."""
        cache = LRUCache(1000)
        assert cache.capacity == 1000

    def test_init_zero_capacity_raises_error(self):
        """Test that zero capacity raises ValueError."""
        with pytest.raises(ValueError, match="Capacity must be greater than 0"):
            LRUCache(0)

    def test_init_negative_capacity_raises_error(self):
        """Test that negative capacity raises ValueError."""
        with pytest.raises(ValueError, match="Capacity must be greater than 0"):
            LRUCache(-5)


class TestLRUCachePut:
    """Test cases for the put method."""

    def test_put_single_item(self):
        """Test putting a single item in cache."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert len(cache) == 1
        assert cache.get("key1") == "value1"

    def test_put_multiple_items(self):
        """Test putting multiple items in cache."""
        cache = LRUCache(5)
        for i in range(5):
            cache.put(f"key{i}", f"value{i}")
        assert len(cache) == 5

    def test_put_update_existing_key(self):
        """Test updating value for existing key."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        cache.put("key1", "value2")
        assert len(cache) == 1
        assert cache.get("key1") == "value2"

    def test_put_evicts_lru_item(self):
        """Test that oldest item is evicted when capacity is exceeded."""
        cache = LRUCache(3)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        cache.put("key4", "value4")  # This should evict key1
        assert len(cache) == 3
        assert cache.get("key1") is None
        assert cache.get("key4") == "value4"

    def test_put_with_integer_keys(self):
        """Test put with integer keys."""
        cache = LRUCache(3)
        cache.put(1, "one")
        cache.put(2, "two")
        assert cache.get(1) == "one"
        assert cache.get(2) == "two"

    def test_put_with_none_value(self):
        """Test putting None as a value."""
        cache = LRUCache(5)
        cache.put("key1", None)
        assert cache.get("key1") is None
        assert "key1" in cache


class TestLRUCacheGet:
    """Test cases for the get method."""

    def test_get_existing_item(self):
        """Test getting an existing item."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_nonexistent_item(self):
        """Test getting a nonexistent item returns None."""
        cache = LRUCache(5)
        assert cache.get("nonexistent") is None

    def test_get_updates_lru_order(self):
        """Test that get updates LRU order."""
        cache = LRUCache(3)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        # Access key1 to make it recently used
        cache.get("key1")
        # Adding key4 should evict key2 (least recently used), not key1
        cache.put("key4", "value4")
        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None
        assert cache.get("key4") == "value4"

    def test_get_multiple_times(self):
        """Test getting same item multiple times."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert cache.get("key1") == "value1"
        assert cache.get("key1") == "value1"

    def test_get_after_update(self):
        """Test getting item after updating it."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        cache.put("key1", "value_updated")
        assert cache.get("key1") == "value_updated"


class TestLRUCacheEviction:
    """Test cases for eviction behavior."""

    def test_eviction_with_capacity_one(self):
        """Test eviction with cache capacity of 1."""
        cache = LRUCache(1)
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        cache.put("key2", "value2")
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    def test_lru_order_with_mixed_operations(self):
        """Test LRU order with mixed get and put operations."""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.get("a")  # a is now most recently used
        cache.put("d", 4)  # b should be evicted (least recently used)
        assert cache.get("a") == 1
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_update_refreshes_position(self):
        """Test that updating a key refreshes its position."""
        cache = LRUCache(3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.put("a", 10)  # Update 'a' to refresh its position
        cache.put("d", 4)  # 'b' should be evicted, not 'a'
        assert cache.get("a") == 10
        assert cache.get("b") is None
        assert cache.get("c") == 3
        assert cache.get("d") == 4


class TestLRUCacheContains:
    """Test cases for the __contains__ method."""

    def test_contains_existing_key(self):
        """Test that __contains__ returns True for existing key."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert "key1" in cache

    def test_contains_nonexistent_key(self):
        """Test that __contains__ returns False for nonexistent key."""
        cache = LRUCache(5)
        assert "nonexistent" not in cache

    def test_contains_after_eviction(self):
        """Test that __contains__ returns False for evicted key."""
        cache = LRUCache(2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        assert "key1" not in cache
        assert "key3" in cache


class TestLRUCacheLen:
    """Test cases for the __len__ method."""

    def test_len_empty_cache(self):
        """Test length of empty cache."""
        cache = LRUCache(5)
        assert len(cache) == 0

    def test_len_after_puts(self):
        """Test length increases with put operations."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert len(cache) == 1
        cache.put("key2", "value2")
        assert len(cache) == 2

    def test_len_at_capacity(self):
        """Test length when cache is at capacity."""
        cache = LRUCache(3)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        assert len(cache) == 3

    def test_len_after_eviction(self):
        """Test length stays at capacity after eviction."""
        cache = LRUCache(2)
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        assert len(cache) == 2

    def test_len_after_update(self):
        """Test length doesn't increase when updating existing key."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        assert len(cache) == 1
        cache.put("key1", "value_new")
        assert len(cache) == 1


class TestLRUCacheRepr:
    """Test cases for the __repr__ method."""

    def test_repr_empty_cache(self):
        """Test string representation of empty cache."""
        cache = LRUCache(5)
        repr_str = repr(cache)
        assert "LRUCache" in repr_str
        assert "OrderedDict()" in repr_str

    def test_repr_with_items(self):
        """Test string representation with items."""
        cache = LRUCache(5)
        cache.put("key1", "value1")
        repr_str = repr(cache)
        assert "LRUCache" in repr_str
        assert "key1" in repr_str


class TestLRUCacheEdgeCases:
    """Test cases for edge cases."""

    def test_empty_string_key(self):
        """Test using empty string as key."""
        cache = LRUCache(5)
        cache.put("", "empty_key_value")
        assert cache.get("") == "empty_key_value"

    def test_complex_values(self):
        """Test storing complex values."""
        cache = LRUCache(5)
        cache.put("list", [1, 2, 3])
        cache.put("dict", {"a": 1, "b": 2})
        cache.put("tuple", (1, 2, 3))
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"a": 1, "b": 2}
        assert cache.get("tuple") == (1, 2, 3)

    def test_overwrite_with_same_value(self):
        """Test overwriting a key with the same value."""
        cache = LRUCache(5)
        cache.put("key", "value")
        cache.put("key", "value")
        assert cache.get("key") == "value"
        assert len(cache) == 1

    def test_many_sequential_puts(self):
        """Test many sequential put operations."""
        cache = LRUCache(10)
        for i in range(20):
            cache.put(f"key{i}", f"value{i}")
        assert len(cache) == 10
        # Should have keys from 10 to 19
        assert cache.get("key9") is None
        assert cache.get("key10") == "value10"
        assert cache.get("key19") == "value19"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
