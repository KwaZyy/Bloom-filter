import io
from unittest.mock import patch

from bloomfilter import BloomFilter, djb2, make_hash_function, sdbm


def test_added_values_are_found() -> None:
    bloom = BloomFilter(50, djb2, sdbm)
    bloom.add("apple")
    bloom.add("banana")

    assert bloom.search("apple")
    assert bloom.search("banana")


def test_missing_value_is_not_reported_for_simple_case() -> None:
    bloom = BloomFilter(100, djb2, make_hash_function(7))
    bloom.add("alpha")
    bloom.add("beta")

    assert not bloom.search("omega")


def test_save_and_load_round_trip() -> None:
    bloom = BloomFilter(64, djb2, sdbm)
    bloom.add_all(["cat", "dog", "otter"])

    buffer = io.BytesIO()

    class BufferContext:
        def __enter__(self) -> io.BytesIO:
            return buffer

        def __exit__(self, exc_type, exc, tb) -> bool:
            return False

    def fake_open(self, mode: str = "r", *args, **kwargs) -> BufferContext:
        if "w" in mode:
            buffer.seek(0)
            buffer.truncate(0)
        else:
            buffer.seek(0)
        return BufferContext()

    with patch("pathlib.Path.mkdir", return_value=None), patch(
        "pathlib.Path.open",
        new=fake_open,
    ), patch("pathlib.Path.exists", return_value=True):
        bloom.save("filter.pkl")
        loaded = BloomFilter.load("filter.pkl", djb2, sdbm)

    assert loaded.m == bloom.m
    assert loaded.filter == bloom.filter
    assert loaded.search("cat")
