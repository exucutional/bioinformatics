import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def read_matrix(filename):
    matrix = defaultdict(lambda: defaultdict(int))
    with open(filename) as fin:
        lines = fin.readlines()
        row_sym = lines[0].split()
        for line in lines[1:]:
            splitline = line.split()
            for i in range(len(splitline[1:])):
                matrix[row_sym[i]][splitline[0]] = int(splitline[i+1])
    
    return matrix


def get_score(s1, s2, score, score_matrix, backtrack, i, j):
    maxscore = -1
    gapscore = 5
    newscore = score[i-1][j] - gapscore
    if newscore > maxscore:
        backtrack[i][j] = 1
        maxscore = newscore

    newscore = score[i][j-1] - gapscore
    if newscore > maxscore:
        backtrack[i][j] = 2
        maxscore = newscore

    newscore = score[i-1][j-1] + score_matrix[s1[i-1]][s2[j-1]]
    if newscore > maxscore:
        backtrack[i][j] = 3
        maxscore = newscore

    if maxscore < 0:
        backtrack[i][j] = 4
        maxscore = 0

    return maxscore


def get_alignment(s1, s2, score, backtrack):
    match = []
    i, j = np.unravel_index(score.argmax(), score.shape)
    while (i > 0 or j > 0) and score[i][j] > 0:
        if backtrack[i, j] == 3:
            match.append([s1[i - 1], s2[j - 1]])
            i -= 1
            j -= 1
        elif backtrack[i, j] == 2:
            match.append(["-", s2[j - 1]])
            j -= 1
        else:
            match.append([s1[i - 1], "-"])
            i -= 1
    match.reverse()
    firstline = []
    secondline = []
    for i in range(len(match)):
        firstline.append(match[i][0])
        secondline.append(match[i][1])

    return ["".join(firstline), "".join(secondline)]



def local_alignment(s1, s2):
    score = np.zeros([len(s1)+1, len(s2)+1], dtype=int)
    backtrack = np.zeros([len(s1)+1, len(s2)+1], dtype=int)
    score_matrix = read_matrix("pam.txt")
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            score[i][j] = get_score(s1, s2, score, score_matrix, backtrack, i, j)
    
    return (np.amax(score), get_alignment(s1, s2, score, backtrack))



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
    rosalind_input = "rosalind_ba5f.txt"
    rosalind_output = "rosalind_ba5f_output.txt"
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
