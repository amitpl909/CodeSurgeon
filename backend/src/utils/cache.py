"""
Cache utilities for CodeSurgeon.
Simple JSON-based caching for MVP.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import UUID

cache_dir = Path(__file__).parent.parent.parent.parent / "backend" / "data" / "cache"
cache_dir.mkdir(parents=True, exist_ok=True)


class CacheManager:
    """Simple JSON-based cache manager."""

    def __init__(self, cache_dir: Path = cache_dir):
        """Initialize cache manager."""
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache: Dict[str, tuple] = {}

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{key}.json"

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in cache.

        Args:
            key: Cache key
            value: Value to cache (must be JSON serializable)
            ttl: Time to live in seconds (None = no expiration)
        """
        try:
            # Store in memory cache with TTL
            expiry = time.time() + ttl if ttl else None
            self.memory_cache[key] = (value, expiry)

            # Also store to file for persistence
            cache_file = self._get_cache_path(key)
            cache_data = {"value": value, "expiry": expiry, "created_at": time.time()}

            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error storing cache: {e}")

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        # Check memory cache first
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if expiry is None or time.time() < expiry:
                return value
            else:
                # Expired, remove from cache
                del self.memory_cache[key]
                return None

        # Try file cache
        try:
            cache_file = self._get_cache_path(key)
            if cache_file.exists():
                with open(cache_file, "r") as f:
                    cache_data = json.load(f)

                value = cache_data.get("value")
                expiry = cache_data.get("expiry")

                # Check if expired
                if expiry and time.time() > expiry:
                    cache_file.unlink()  # Delete expired file
                    return None

                return value
        except Exception as e:
            print(f"Error reading cache: {e}")

        return None

    def delete(self, key: str) -> None:
        """Delete cache entry.

        Args:
            key: Cache key
        """
        # Remove from memory
        if key in self.memory_cache:
            del self.memory_cache[key]

        # Remove file
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            cache_file.unlink()

    def clear(self) -> None:
        """Clear all cache."""
        # Clear memory
        self.memory_cache.clear()

        # Clear files
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


# Global cache instance
cache = CacheManager()
