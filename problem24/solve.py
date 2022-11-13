import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def get_score(s1, s2, score, backtrack, i, j):
    maxscore = -1000
    gapscore = 1
    newscore = score[i-1][j]-gapscore
    if newscore > maxscore:
        backtrack[i][j] = 1
        maxscore = newscore

    newscore = score[i][j-1]-gapscore
    if newscore > maxscore:
        backtrack[i][j] = 2
        maxscore = newscore

    if s1[i-1] == s2[j-1]:
        newscore = score[i-1][j-1]+1
    else:
        newscore = score[i-1][j-1]-1

    if newscore > maxscore:
        backtrack[i][j] = 3
        maxscore = newscore

    return maxscore


def get_alignment(s1, s2, score, backtrack):
    res1 = ""
    res2 = ""
    i = np.argmax(score[:, len(s2)])
    j = len(s2)
    while i > 0 or j > 0:
        if backtrack[i, j] == 3:
            i -= 1
            j -= 1
            res1 = s1[i]+res1
            res2 = s2[j]+res2
        elif backtrack[i, j] == 2:
            j -= 1
            res1 = "-"+res1
            res2 = s2[j]+res2
        elif backtrack[i][j] == 1:
            i -= 1
            res1 = s1[i]+res1
            res2 = "-"+res2
        else:
            i = 0
            j = 0


    return [res1, res2]


def init(score, backtrack):
    for j in range(1, score.shape[1]):
        score[0][j] = score[0][j-1]-1
        backtrack[0][j] = 2


def local_alignment(s1, s2):
    score = np.zeros([len(s1)+1, len(s2)+1], dtype=int)
    backtrack = np.zeros([len(s1)+1, len(s2)+1], dtype=int)
    init(score, backtrack)
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            score[i][j] = get_score(s1, s2, score, backtrack, i, j)
    
    return (np.amax(score[-1, :]), get_alignment(s1, s2, score, backtrack))


def solve(s1, s2):
    return local_alignment(s1, s2)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        s1 = lines[0].strip()
        s2 = lines[1].strip()
        answer = solve(s1, s2)
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
            expected = (int(lines[0]), [lines[1].strip(), lines[2].strip()])
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba5h.txt"
    rosalind_output = "rosalind_ba5h_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(str(answer[0])+"\n")
        fout.write(str(answer[1][0])+"\n")
        fout.write(str(answer[1][1])+"\n")
    
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
