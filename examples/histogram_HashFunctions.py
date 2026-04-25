from src.HashingFunctions import lose_lose, djb2, sdbm, distribution
from functools import partial
import mmh3

seeded_mmh3 = partial(mmh3.hash, seed=815, signed=False)
m1 = 200000
m2 = 700000
distribution("words.txt", lose_lose, m1)
distribution("words.txt", djb2, m1)
distribution("words.txt", sdbm, m1)
distribution("words.txt", seeded_mmh3, m1)
print("\n")
distribution("DNA.txt", lose_lose, m2)
distribution("DNA.txt", djb2, m2)
distribution("DNA.txt", sdbm, m2)
distribution("DNA.txt", seeded_mmh3, m2)
