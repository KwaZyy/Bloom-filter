import itertools


def generate_dna_sequences(max_length, output_file):
    nucleotides = ['A', 'C', 'G', 'T']
    with open(output_file, 'w') as f:
        for length in range(1, max_length + 1):
            for sequence in itertools.product(nucleotides, repeat=length):
                f.write(''.join(sequence) + '\n')

generate_dna_sequences(10, "DNA.txt")
