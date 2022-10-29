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


def solve(total_mass):
    masses = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
    arr = [0]*(total_mass+1)
    arr[0] = 1
    for mass in range(total_mass+1):
        sum = 0
        for peptideM in masses:
            if mass >= peptideM:
                sum += arr[mass-peptideM]
        
        arr[mass] += sum
    
    return arr[total_mass]


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        total_mass = int(lines[0].strip())
        answer = solve(total_mass)
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
            expected = int(fout.readline())
            passed = expected == answer
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba4d.txt"
    rosalind_output = "rosalind_ba4d_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(str(answer))
    
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