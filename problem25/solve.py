import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def get_score(s1, s2, s3, score, backtrack, i, j, k):
    testscore = -999
    maxscore = -999
    if s1[i-1] == s2[j-1] == s3[k-1]:
        testscore = score[i-1][j-1][k-1]+1
    else:
        testscore = score[i-1][j-1][k-1]

    if testscore > maxscore:
        backtrack[i][j][k] = 0
        maxscore = testscore

    testscore = score[i-1][j][k]
    if testscore > maxscore:
        backtrack[i][j][k] = 1
        maxscore = testscore

    testscore = score[i][j-1][k]
    if testscore > maxscore:
        backtrack[i][j][k] = 2
        maxscore = testscore

    testscore = score[i][j][k-1]
    if testscore > maxscore:
        backtrack[i][j][k] = 3
        maxscore = testscore

    testscore = score[i-1][j-1][k]
    if testscore > maxscore:
        backtrack[i][j][k] = 4
        maxscore = testscore

    testscore = score[i-1][j][k-1]
    if testscore > maxscore:
        backtrack[i][j][k] = 5
        maxscore = testscore

    testscore = score[i][j-1][k-1]
    if testscore > maxscore:
        backtrack[i][j][k] = 6
        maxscore = testscore

    return maxscore


def get_alignment(s1, s2, s3, backtrack):
    res1 = ""
    res2 = ""
    res3 = ""
    i = len(s1)
    j = len(s2)
    k = len(s3)
    def addsym(index, res, sym):
        return index-1, sym[index-1]+res

    while i > 0 or j > 0 or k > 0:
        if backtrack[i][j][k] == 0:
            i, res1 = addsym(i, res1, s1)
            j, res2 = addsym(j, res2, s2)
            k, res3 = addsym(k, res3, s3)
        if backtrack[i][j][k] == 1:
            i, res1 = addsym(i, res1, s1)
            res2 = "-"+res2
            res3 = "-"+res3
        if backtrack[i][j][k] == 2:
            res1 = "-"+res1
            j, res2 = addsym(j, res2, s2)
            res3 = "-"+res3
        if backtrack[i][j][k] == 3:
            res1 = "-"+res1
            res2 = "-"+res2
            k, res3 = addsym(k, res3, s3)
        if backtrack[i][j][k] == 4:
            i, res1 = addsym(i, res1, s1)
            j, res2 = addsym(j, res2, s2)
            res3 = "-"+res3
        if backtrack[i][j][k] == 5:
            i, res1 = addsym(i, res1, s1)
            res2 = "-"+res2
            k, res3 = addsym(k, res3, s3)
        if backtrack[i][j][k] == 6:
            res1 = "-"+res1
            j, res2 = addsym(j, res2, s2)
            k, res3 = addsym(k, res3, s3)

    return [res1, res2, res3]


def init(backtrack, s1, s2, s3):
    for i in range(1, len(s1)+1):
        backtrack[i][0][0] = 1
        for j in range(1, len(s2)+1):
            backtrack[i][j][0] = 4
        for j in range(1, len(s3)+1):
            backtrack[i][0][j] = 5
    for i in range(1, len(s2)+1):
        backtrack[0][i][0] = 2
        for j in range(len(s3)+1):
            backtrack[0][i][j] = 6
    for i in range(1, len(s3)+1):
        backtrack[0][0][i] = 3
    


def local_alignment(s1, s2, s3):
    score = np.zeros([len(s1)+1, len(s2)+1, len(s3)+1], dtype=int)
    backtrack = np.zeros([len(s1)+1, len(s2)+1, len(s3)+1], dtype=int)
    init(backtrack, s1, s2, s3)
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            for k in range(1, len(s3)+1):
                score[i][j][k] = get_score(s1, s2, s3, score, backtrack, i, j, k)
    
    return (np.amax(score), get_alignment(s1, s2, s3, backtrack))



def solve(s1, s2, s3):
    return local_alignment(s1, s2, s3)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        s1 = lines[0].strip()
        s2 = lines[1].strip()
        s3 = lines[2].strip()
        answer = solve(s1, s2, s3)
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
            expected = (int(lines[0]), [lines[1].strip(), lines[2].strip(), lines[3].strip()])
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba5m.txt"
    rosalind_output = "rosalind_ba5m_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(str(answer[0])+"\n")
        fout.write(str(answer[1][0])+"\n")
        fout.write(str(answer[1][1])+"\n")
        fout.write(str(answer[1][2])+"\n")

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
