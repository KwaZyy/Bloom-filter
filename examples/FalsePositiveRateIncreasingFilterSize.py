from src.BloomFilterPlots import false_positive_against_filter_size

false_positive_against_filter_size("words.txt", 30000, 1000000, k=3, samples=25)
false_positive_against_filter_size("DNA.txt", 200000, 3000000, k=5, samples=25)
