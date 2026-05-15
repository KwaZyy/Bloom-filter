from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3


def test_hash_functions_return_integers():
    for hash_function in [lose_lose, dj2 if False else djb2, sdbm, MurmurHash3]:
        assert isinstance(hash_function("hello"), int)


def test_hash_functions_are_deterministic():
    for hash_function in [lose_lose, djb2, sdbm, MurmurHash3]:
        assert hash_function("hello") == hash_function("hello")


def test_hash_functions_change_for_different_strings():
    for hash_function in [lose_lose, djb2, sdbm, MurmurHash3]:
        assert hash_function("hello") != hash_function("world")


def test_hash_functions_work_for_dna_strings():
    dna_string = "ACGTACGT"
    for hash_function in [lose_lose, djb2, sdbm, MurmurHash3]:
        assert isinstance(hash_function(dna_string), int)
