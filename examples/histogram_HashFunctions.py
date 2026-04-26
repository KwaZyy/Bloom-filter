from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3, distribution

m1 = 200000
m2 = 700000
distribution("words.txt", lose_lose, m1)
distribution("words.txt", djb2, m1)
distribution("words.txt", sdbm, m1)
distribution("words.txt", MurmurHash3, m1)
print("\n")
distribution("DNA.txt", lose_lose, m2)
distribution("DNA.txt", djb2, m2)
distribution("DNA.txt", sdbm, m2)
distribution("DNA.txt", MurmurHash3, m2)
