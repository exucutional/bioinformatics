from itertools import cycle, permutations
from operator import length_hint
import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def chromosome_to_cycle(chromosome):
    nodes = [0]*len(chromosome)*2
    for i in range(len(chromosome)):
        if chromosome[i] > 0:
            nodes[2*i]   = 2*chromosome[i]-1
            nodes[2*i+1] = 2*chromosome[i]
        else:
            nodes[2*i]   = -2*chromosome[i]
            nodes[2*i+1] = -2*chromosome[i]-1

    return nodes


def cycle_to_chromosome(cycle):
    chromosome = []
    for i in range(len(cycle)//2):
        if cycle[2*i] < cycle[2*i+1]:
            chromosome.append(cycle[2*i+1]//2)
        else:
            chromosome.append(-cycle[2*i]//2)

    return chromosome


def coloured_edges(genome):
    edges = set()
    for chromosome in genome:
        nodes = chromosome_to_cycle(chromosome)
        nodes.append(nodes[0])
        for i in range(len(chromosome)):
            edges.add((nodes[2*i+1], nodes[2*i+2]))

    return edges


def genome_graph_to_cycles(genome_graph):
    cycles = []
    cycle = []
    cycle_edges = genome_graph.copy()
    cycle_edge = cycle_edges.pop()
    while cycle_edge:
        if cycle_edge[0]%2 == 0:
            cycle += [cycle_edge[0]-1, cycle_edge[0]]
        else:
            cycle += [cycle_edge[0]+1, cycle_edge[0]]

        next_node = 0
        if cycle_edge[1]%2 == 0:
            next_node = cycle_edge[1]-1
        else:
            next_node = cycle_edge[1]+1

        cycle_edge = None
        for edge in cycle_edges:
            if edge[0] == next_node:
                cycle_edge = edge
                break

        if cycle_edge:
            cycle_edges.remove(cycle_edge)
        else:
            cycles.append(cycle[:])
            cycle = []
            if cycle_edges:
                cycle_edge = cycle_edges.pop()

    return cycles


def groupNodes(genome_graph):
    parent = dict()
    rank = dict()
    for e in genome_graph:
        parent[e[0]] = e[0]
        parent[e[1]] = e[1]
        rank[e[0]] = 0
        rank[e[1]] = 0

    def findParent(i):
        if i != parent[i]:
            parent[i] = findParent(parent[i])
        return parent[i]
    
    def union(i, j):
        i_id = findParent(i)
        j_id = findParent(j)
        if i_id == j_id:
            return
        if rank[i_id] > rank[j_id]:
            parent[j_id] = i_id
        else:
            parent[i_id] = j_id
            if rank[i_id] == rank[j_id]:
                rank[j_id] += 1
    
    def unionEdges(edge):
        union(edge[0], edge[1])
        if 1 == edge[0] % 2:
            union(edge[0], edge[0]+1)
        else:
            union(edge[0], edge[0]-1)

        if 1 == edge[1] % 2:
            union(edge[1], edge[1]+1)
        else:
            union(edge[1], edge[1]-1)

    for e in genome_graph:
        unionEdges(e)

    nodesID = dict()
    nodesSets = set()

    for e in genome_graph:
        id = findParent(e[0])
        nodesID[e[0]] = id
        nodesID[e[1]] = id
        nodesSets.add(id)
    
    return nodesSets, nodesID


def buildEdgeDict(genome_graph, nodesID):
    edgeDict = dict()
    for e in genome_graph:
        id = nodesID[e[0]]
        if not id in edgeDict:
            edgeDict[id] = dict()
        edgeDict[id][e[0]] = e[1]
        edgeDict[id][e[1]] = e[0]
    return edgeDict


def graph_to_genome(genome_graph):
    nodesSet, nodesID = groupNodes(genome_graph)
    edgeDict = buildEdgeDict(genome_graph, nodesID)
    nodesDict = dict()
    for id, eDict in edgeDict.items():
        nodesDict[id] = []
        currNode0 = list(eDict)[0]
        while len(eDict) > 0:
            nodesDict[id].append(currNode0)
            if 1 == currNode0 % 2:
                currNode1 = currNode0+1
            else:
                currNode1 = currNode0-1
            nodesDict[id].append(currNode1)
            newNode = eDict[currNode1]
            del eDict[currNode0]
            del eDict[currNode1]
            currNode0 = newNode
    newGenome = dict()
    for id, nodes in nodesDict.items():
        newGenome[id] = cycle_to_chromosome(nodes)
    newGenome = sorted(newGenome.values(), key = lambda x:abs(x[0]))
    return newGenome


def graph_to_genome2(genome_graph):
    genome = set()
    for cycle in genome_graph_to_cycles(genome_graph):
        genome.add(cycle_to_chromosome(cycle))

    return genome


def genome_to_graph(genome):
    return coloured_edges(genome)


def two_break_on_genome_graph(genome_graph, i1, i2, j1, j2):
    genome_graph.discard((i1, i2))
    genome_graph.discard((i2, i1))
    genome_graph.discard((j1, j2))
    genome_graph.discard((j2, j1))
    genome_graph.add((i1, j1))
    genome_graph.add((i2, j2))


def two_break_on_genome(genome, i1, i2, j1, j2):
    genome_graph = genome_to_graph(genome)
    two_break_on_genome_graph(genome_graph, i1, i2, j1, j2)
    return graph_to_genome(genome_graph)


def genome_to_string(genome):
    res = ""
    for chromosome in genome:
        res += "(" + " ".join([("+" if i > 0 else "")+str(i) for i in chromosome]) + ") "

    return res


def solve(genome, i1, i2, j1, j2):
    return two_break_on_genome(genome, i1, i2, j1, j2)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        genome = []
        chromosome = []
        for c in lines[0].strip().split(")("):
            for p in c.split():
                if p.startswith("("):
                    chromosome.append(int(p[1:]))
                elif p.endswith(")"):
                    chromosome.append(int(p[:-1]))
                else:
                    chromosome.append(int(p))

            genome.append(chromosome[:])
            chromosome = []

        args = lines[1].strip().split(", ")
        i1 = int(args[0])
        i2 = int(args[1])
        j1 = int(args[2])
        j2 = int(args[3])
        answer = solve(genome, i1, i2, j1, j2)
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
        answer = genome_to_string(read_and_solve(os.path.join(input_dir, f"input_{i}.txt")))
        end = time.time()
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            lines = fout.readlines()
            expected = lines[0].strip()
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba6k.txt"
    rosalind_output = "rosalind_ba6k_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(genome_to_string(answer))

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
