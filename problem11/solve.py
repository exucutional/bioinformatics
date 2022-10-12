import os
import time

def solve_rec(adjlist, res, u):
    stack = adjlist[u]
    while len(stack) != 0:
        v = stack.pop()
        solve_rec(adjlist, res, v)
        res.append(v)


def solve(adjlist, begin, end):
    res = []
    adjlist[begin].append(end)
    solve_rec(adjlist, res, begin)
    return res[::-1]


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        adjlist = [[] for _ in range(len(lines)+2)]
        inoutlist = [[0, 0] for _ in range(len(lines)+2)]
        for line in lines:
            vertices = line.split("->")
            v = int(vertices[0].strip())
            adjlist[v] = [int(adj) for adj in vertices[1].split(',')]
            inoutlist[v][1] += len(adjlist[v])
            for adjv in adjlist[v]:
                inoutlist[adjv][0] += 1

        begin = 0
        end = 0
        for i, inout in enumerate(inoutlist):
            if inout[0] + 1 == inout[1]:
                end = i
            
            if (inout[0] == inout[1] + 1):
                begin = i

        answer = solve(adjlist, begin, end)
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
            expected = [int(v) for v in fout.readline().split("->")]
            passed = answer == expected
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba3f.txt"
    rosalind_output = "rosalind_ba3f_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write("->".join([str(i) for i in answer]))
    
    print("Done")


#test()
solve_problem()
