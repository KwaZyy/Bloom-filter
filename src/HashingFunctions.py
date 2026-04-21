def lose_lose(s: str) -> int:
    """Implementation of loselose hash function."""
    h = 0
    for char in s:
        h += ord(char)
    return h


def djb2(s: str) -> int:
    """Implementation of the djb2 hash function."""
    h = 5381
    for char in s:
        h = ((h << 5) + h) + ord(char)  # h = h * 33 + ord(char)
    return h


def sdbm(s: str) -> int:
    """Implementation of the sdbm hash function."""
    h = 0
    for char in s:
        h = ord(char) + (h << 6) + (h << 16) - h
    return h
