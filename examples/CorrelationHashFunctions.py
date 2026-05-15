from src.HashingFunctions import lose_lose, djb2, sdbm, MurmurHash3, correlation_plot

m1 = 200000
m2 = 700000

correlation_plot("words.txt", lose_lose, djb2, m1)
correlation_plot("words.txt", lose_lose, sdbm, m1)
correlation_plot("words.txt", lose_lose, MurmurHash3, m1)
correlation_plot("words.txt", djb2, sdbm, m1)
correlation_plot("words.txt", djb2, MurmurHash3, m1)
correlation_plot("words.txt", sdbm, MurmurHash3, m1)

correlation_plot("DNA.txt", lose_lose, djb2, m2)
correlation_plot("DNA.txt", lose_lose, sdbm, m2)
correlation_plot("DNA.txt", lose_lose, MurmurHash3, m2)
correlation_plot("DNA.txt", djb2, sdbm, m2)
correlation_plot("DNA.txt", djb2, MurmurHash3, m2)
correlation_plot("DNA.txt", sdbm, MurmurHash3, m2)
