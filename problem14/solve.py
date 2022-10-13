from collections import defaultdict
import os
import sys
import time

from argparse import ArgumentParser

def get_Bruijin_adj(patterns):
    adjdict = defaultdict(list)
    for p in patterns:
        l = p[:-1]
        r = p[1:]
        adjdict[l].append(r)
        if r not in adjdict:
            adjdict[r] = []

    return adjdict


def get_inout(adjdict):
    indict = defaultdict(int)
    outdict = defaultdict(int)
    for v, adjvs in adjdict.items():
        outdict[v] = len(adjvs)
        for adjv in adjvs:
            indict[adjv] += 1

        if adjv not in outdict:
            outdict[adjv] = 0

    return indict, outdict


def contigs(adjdict, v, indict, outdict):
    res = []
    for n in adjdict[v]:
        path = [v, n]
        ins = indict[n]
        outs = outdict[n]
        while ins == 1 and outs == 1:
            n = adjdict[n][0]
            path.append(n)
            ins = indict[n]
            outs = outdict[n]

        res.append(path)

    return res


def build_contigs(path):
    sequence = path[0]
    for kmer in path[1:]:
        sequence += kmer[-1]

    return sequence


def solve(patterns):
    adjdict = get_Bruijin_adj(patterns)
    paths = []
    indict, outdict = get_inout(adjdict)
    for v in outdict:
        ins = indict[v]
        outs = outdict[v]
        if not (outs == 1 and ins == 1) and outs > 0:
            paths.extend(contigs(adjdict, v, indict, outdict))


    return [build_contigs(p) for p in paths]


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        patterns = []
        for line in lines:
            patterns.append(line.strip())

        answer = solve(patterns)
        return answer


def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    skip = [2]
    for i in range(1, files_n+1):
        if i in skip:
            print(f"-> Test {i} skipped")
            continue

        start = time.time()
        answer = read_and_solve(os.path.join(input_dir, f"input_{i}.txt"))
        end = time.time()
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            expected = [l.strip() for l in fout.readlines()]
            passed = answer == expected
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba3k.txt"
    rosalind_output = "rosalind_ba3k_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(' '.join(answer))
    
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