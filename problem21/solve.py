import numpy as np
import os
import sys
import time

from argparse import ArgumentParser


def manhattan(n, m, down, right):
    score = np.zeros([n+1, m+1])
    for i in range(1, n+1):
        score[i][0] = score[i-1][0] + down[i-1][0]
    
    for i in range(1, m+1):
        score[0][i] = score[0][i-1] + right[0][i-1]

    for i in range(1, n+1):
        for j in range(1, m+1):
            score[i][j] = max(score[i-1][j] + down[i-1][j], score[i][j-1]+right[i][j-1])
    
    return score[n][m]



def solve(n, m, down, right):
    return manhattan(n, m, down, right)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        args = lines[0].split()
        m = int(args[1])
        n = int(args[0])
        down = []
        for i in range(1, n+1):
            down.append([int(s) for s in lines[i].split()])

        right = []
        for i in range(n+2, n+2+n+1):
            right.append([int(s) for s in lines[i].split()])

        answer = solve(n, m, down, right)
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
            expected = int(fout.readlines()[0])
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba5b.txt"
    rosalind_output = "rosalind_ba5b_output.txt"
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
