from collections import defaultdict
import os
import sys
import time

from argparse import ArgumentParser

sys.setrecursionlimit(5000)

def euler_path_rec(adjlist, res, u):
    stack = adjlist[u]
    while len(stack) != 0:
        v = stack.pop()
        euler_path_rec(adjlist, res, v)
        res.append(v)


def get_begin_end(adjlist):
    inoutlist = [[0, 0] for _ in range(len(adjlist))]
    for v, adjvs in enumerate(adjlist):
        inoutlist[v][1] += len(adjvs)
        for adjv in adjvs:
            inoutlist[adjv][0] += 1

    begin = 0
    end = 0
    for i, inout in enumerate(inoutlist):
        if inout[0] + 1 == inout[1]:
            end = i

        if (inout[0] == inout[1] + 1):
            begin = i

    return begin, end


def euler_path(adjlist):
    res = []
    begin, end = get_begin_end(adjlist)
    adjlist[begin].append(end)
    euler_path_rec(adjlist, res, begin)
    return res[::-1]


def get_Bruijin_adj(k, patterns):
    adjdict = defaultdict(list)
    for p in patterns:
        l = tuple([p[0][:k-1], p[1][:k-1]])
        r = tuple([p[0][1:], p[1][1:]])
        adjdict[l].append(r)
        if r not in adjdict:
            adjdict[r] = []
    
    adjlist = [[] for _ in range(len(adjdict))]
    ivmap = {}
    vimap = {}
    i = 0
    for v, adjvs in adjdict.items():
        if v not in vimap:
            ivmap[i] = v
            vimap[v] = i
            i += 1

        for adjv in adjvs:
            if adjv not in vimap:
                ivmap[i] = adjv
                vimap[adjv] = i
                i += 1

            adjlist[vimap[v]].append(vimap[adjv])
        

    return adjlist, ivmap 


def string_spelled_by_gapped_patterns(patterns, k, d):
    first = patterns[0][0] + ''.join(p[0][-1] for p in patterns[1:])
    second = patterns[0][1] + ''.join(p[1][-1] for p in patterns[1:])
    return first + second[-(k+d):]


def solve(k, d, patterns):
    adjlist, ivmap = get_Bruijin_adj(k, patterns)
    path = [ivmap[i] for i in euler_path(adjlist)]
    return string_spelled_by_gapped_patterns(path, k, d)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        args = lines[0].strip().split()
        k = int(args[0])
        d = int(args[1])
        patterns = []
        for line in lines[1:]:
            patterns.append(tuple(line.strip().split('|')))

        answer = solve(k, d, patterns)
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
            expected = fout.readline().strip()
            passed = answer == expected
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba3j.txt"
    rosalind_output = "rosalind_ba3j_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(answer)
    
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