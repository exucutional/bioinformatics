from itertools import cycle, permutations
from operator import length_hint
import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def get_breakpoint_graph(genome1, genome2):
    bgraph = defaultdict(list)
    for chromosome in genome1 + genome2:
        for i in range(len(chromosome)):
            next_i = (i+1)%len(chromosome)
            bgraph[chromosome[i]].append(-1*chromosome[next_i])
            bgraph[-1*chromosome[next_i]].append(chromosome[i])

    return bgraph


def get_cycles_n(bgraph):
    cycles_n = 0
    nodes = set(bgraph.keys())
    while nodes:
        cycle_nodes = set([nodes.pop()])
        while cycle_nodes:
            node = cycle_nodes.pop()
            neighbours = set(neighbour for neighbour in bgraph[node] if neighbour in nodes)
            cycle_nodes = cycle_nodes.union(neighbours)
            nodes = nodes.difference(neighbours)
        
        cycles_n += 1

    return cycles_n



def get_blocks_n(genome):
    blocks_n = 0
    for chromosome in genome:
        blocks_n += len(chromosome)
    
    return blocks_n


def two_break_distance(genome1, genome2):
    bgraph = get_breakpoint_graph(genome1, genome2)
    cycles_n = get_cycles_n(bgraph)
    blocks_n = get_blocks_n(genome1)
    return blocks_n - cycles_n


def solve(genome1, genome2):
    return two_break_distance(genome1, genome2)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        genome1 = []
        genome2 = []
        chromosome = []
        for c in lines[0].strip().split(")("):
            for p in c.split():
                if p.startswith("("):
                    chromosome.append(int(p[1:]))
                elif p.endswith(")"):
                    chromosome.append(int(p[:-1]))
                else:
                    chromosome.append(int(p))

            genome1.append(chromosome[:])
            chromosome = []

        for c in lines[1].strip().split(")("):
            for p in c.split():
                if p.startswith("("):
                    chromosome.append(int(p[1:]))
                elif p.endswith(")"):
                    chromosome.append(int(p[:-1]))
                else:
                    chromosome.append(int(p))

            genome2.append(chromosome)
            chromosome = []

        answer = solve(genome1, genome2)
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
            expected = int(lines[0].strip())
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba6c.txt"
    rosalind_output = "rosalind_ba6c_output.txt"
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
