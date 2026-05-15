from src.BloomFilter import BloomFilter, KMBloomFilter, false_positive_rate
from src.HashingFunctions import sdbm, MurmurHash3


def test_empty_filter_returns_false_for_unknown_string():
    bloom_filter = BloomFilter(100, sdbm)
    assert bloom_filter.search("hello") is False


def test_added_string_can_be_found():
    bloom_filter = BloomFilter(100, sdbm)
    bloom_filter.add("hello")
    assert bloom_filter.search("hello") is True


def test_added_list_of_strings_can_be_found():
    bloom_filter = BloomFilter(100, sdbm)
    strings = ["apple", "banana", "cherry"]
    bloom_filter.add(strings)

    for string in strings:
        assert bloom_filter.search(string) is True


def test_km_bloom_filter_added_string_can_be_found():
    bloom_filter = KMBloomFilter(1000, sdbm, MurmurHash3, 3)
    bloom_filter.add("DNA_string")
    assert bloom_filter.search("DNA_string") is True


def test_inserted_strings_have_no_false_negatives():
    bloom_filter = KMBloomFilter(1000, sdbm, MurmurHash3, 3)
    inserted_strings = ["AAA", "CCC", "GGG", "TTT"]
    bloom_filter.add(inserted_strings)

    for string in inserted_strings:
        assert bloom_filter.search(string) is True


def test_false_positive_rate_is_between_zero_and_one():
    bloom_filter = KMBloomFilter(1000, sdbm, MurmurHash3, 3)
    all_strings = ["AAA", "CCC", "GGG", "TTT", "ACG", "TGA"]
    inserted_strings = ["AAA", "CCC", "GGG"]

    rate = false_positive_rate(bloom_filter, all_strings, inserted_strings)

    assert 0 <= rate <= 1
