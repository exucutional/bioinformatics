from itertools import permutations
import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def get_reverse(permutation, i, j):
    reverse = [i*-1 for i in reversed(permutation[i:j+1])]
    return permutation[:i] + reverse + permutation[j+1:]


def greedy_sort(permutation):
    res = []
    for i in range(len(permutation)):
        if i != abs(permutation[i])-1:
            for j in range(i+1, len(permutation)):
                if i == abs(permutation[j])-1:
                    permutation = get_reverse(permutation, i, j)
                    res.append(permutation[:])
        if i == -permutation[i]-1:
            permutation[i] *= -1
            res.append(permutation[:])
    
    return res


def solve(permutation):
    return greedy_sort(permutation)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        permutation = [int(i) for i in lines[0].strip()[1:-1].split()]
        answer = solve(permutation)
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
            lines = fout.readlines()
            expected = [[int(i) for i in line.strip()[1:-1].split()] for line in lines]
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba6a.txt"
    rosalind_output = "rosalind_ba6a_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        for p in answer: 
            fout.write("(" + " ".join([("+" if i > 0 else "")+str(i) for i in p])+")\n")

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
