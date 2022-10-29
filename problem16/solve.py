from collections import defaultdict
import os
import sys
import time

from argparse import ArgumentParser

sys.setrecursionlimit(2000)


amino_to_code = {
    'M': set(["AUG"]),
    'I': set(["AUU", "AUC", "AUA"]),
    'R': set(["AGG", "AGA"]),
    'S': set(["AGC", "AGU"]),
    'T': set(["ACG", "ACA", "ACU", "ACC"]),
    'K': set(["AAG", "AAA"]),
    'N': set(["AAC", "AAU"]),
    'L': set(["UUG", "UUA"]),
    'F': set(["UUC", "UUU"]),
    'W': set(["UGG"]),
    '*': set(["UGA", "UAG", "UAA"]),
    'C': set(["UGC", "UGU"]),
    'S': set(["UCG", "UCU", "UCA", "UCC"]),
    'Y': set(["UAC", "UAU"]),
    'V': set(["GUG", "GUC", "GUA", "GUU"]),
    'G': set(["GGG", "GGC", "GGA", "GGU"]),
    'A': set(["GCG", "GCA", "GCU", "GCC"]),
    'E': set(["GAA", "GAG"]),
    'D': set(["GAU", "GAC"]),
    'L': set(["CUU", "CUA", "CUC", "CUG"]),
    'R': set(["CGU", "CGG", "CGA", "CGC"]),
    'P': set(["CCC", "CCU", "CCG", "CCA"]),
    'Q': set(["CAA", "CAG"]),
    'H': set(["CAU", "CAC"])
}


def complement_reverse(dna):
    res = ""
    for c in dna[::-1]:
        if c == 'T':
            res += 'A'
        if c == 'A':
            res += 'T'
        if c == 'G':
            res += 'C'
        if c == 'C':
            res += 'G'
    
    return res


def transcribe_codon(codon):
    transcribed = ""
    for c in codon:
        if c == 'T':
            transcribed += 'U'
        else:
            transcribed += c

    return transcribed


def encode_pattern(pattern):
    amino_str = ""
    k = 0
    while k < len(pattern)-3+1:
        codon = pattern[k:k+3]
        for amino, patterns in amino_to_code.items():
            if amino == '*' and codon in patterns:
                return amino_str
            if codon in patterns:
                amino_str += amino

        k += 3
    
    return amino_str


def start_transcription(dna, amino, res):
    k = 0
    while k < len(dna)-3*len(amino)+1:
        pattern = dna[k:k+3*len(amino)]
        amino_cand = encode_pattern(transcribe_codon(pattern))
        amino_cand_r = encode_pattern(transcribe_codon(complement_reverse(pattern)))
        if amino_cand == amino or amino_cand_r == amino:
            res.append(pattern)

        k += 1


def solve(dna, amino):
    res = []
    complement_reverse_dna = complement_reverse(dna)
    start_transcription(dna, amino, res)
    #start_transcription(complement_reverse_dna, amino[::-1], res)
    #start_transcription(dna[1:], amino, res)
    #start_transcription(complement_reverse_dna[1:], amino[::-1], res)
    #start_transcription(dna[2:], amino, res)
    #start_transcription(complement_reverse_dna[2:], amino[::-1], res)
    return res


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        dna = lines[0].strip()
        amino = lines[1].strip()
        answer = solve(dna, amino)
        return answer


def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    skip = []
    for i in range(1, files_n+1):
        if i in skip:
            print(f"-> Test {i} skipped")
            continue

        start = time.time()
        answer = read_and_solve(os.path.join(input_dir, f"input_{i}.txt"))
        end = time.time()
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            expected = [line.strip() for line in fout.readlines()]
            passed = True
            for e in expected:
                if answer.count(e) != expected.count(e):
                    passed = False
                    break
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba4b.txt"
    rosalind_output = "rosalind_ba4b_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write("\n".join(answer))
    
    print("Done")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--solve", action="store_true", dest="solve", default=False,
                    help="Solve")
    parser.add_argument("-t", "--test", action="store_true", dest="test", default=False,
                    help="Test")

    args = parser.parse_args()
    if args.test:
        test()
    
    if args.solve:
        solve_problem()