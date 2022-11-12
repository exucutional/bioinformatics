import numpy as np
import os
import sys
import time
from collections import defaultdict
import copy
from argparse import ArgumentParser


def get_reachable(src, adj):
    reachable = []
    left = [src]
    while left:
        next = left.pop()
        reachable.append(next)
        for child in adj[next]["out"]:
            left.append(child)
    
    return list(set(reachable))


def get_no_incoming(adj):
    nodes = []
    for node in adj:
        if "in" not in adj[node] or not adj[node]["in"]:
            nodes.append(node)

    return nodes


def topological_sort(adj):
    adj_c = copy.deepcopy(adj)
    sorted = []
    no_incoming = get_no_incoming(adj)
    while no_incoming:
        node = no_incoming.pop()
        sorted.append(node)
        while adj_c[node]["out"]:
            node_c = adj_c[node]["out"].pop()
            adj_c[node_c]["in"].remove((node))
            if not adj_c[node_c]["in"]:
                no_incoming.append(node_c)

    return sorted


def score_init(adj, sorted_reachable):
    score = dict()
    for node in get_no_incoming(adj):
        if node in sorted_reachable:
            score[node] = 0
            sorted_reachable.remove(node)
    
    return score


def trim_adj(adj, reachable):
    for node in reachable:
        newnodes = [newnode_w for newnode_w in adj[node]["out"] if newnode_w in reachable]
        adj[node]["out"] = newnodes
        newnodes = [newnode_w for newnode_w in adj[node]["in"] if newnode_w in reachable]
        adj[node]["in"] = newnodes


def max_income(score, node, adj, weights, backrack):
    max_score = 0
    for node_in in adj[node]["in"]:
        new_score = score[node_in] + weights[node_in][node]
        if max_score < new_score:
            max_score = new_score
            backrack[node] = node_in

    return max_score


def trace(src, dst, backtrack):
    track = [dst]
    node = backtrack[dst]
    while node:
        track.append(node)
        if node == src:
            break
        else:
            node = backtrack[node]

    track.reverse()
    return track


def longest_dag_path(src, dst, adj, weights):
    reachable = get_reachable(src, adj)
    sorted_adj = topological_sort(adj)
    sorted_reachable = [node for node in sorted_adj if node in reachable]
    score = score_init(adj, sorted_reachable)
    backtrack = dict()
    trim_adj(adj, reachable)
    for node in sorted_reachable:
        score[node] = max_income(score, node, adj, weights, backtrack)

    return (score[dst], [src] + trace(src, dst, backtrack))



def solve(src, dst, adj, weights):
    return longest_dag_path(src, dst, adj, weights)


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        src = int(lines[0])
        dst = int(lines[1])
        adj = defaultdict(lambda: defaultdict(list))
        weights = defaultdict(lambda: defaultdict(int))
        for l in lines[2:]:
            from_to_w = l.split()
            adj[int(from_to_w[0])]["out"].append(int(from_to_w[1]))
            adj[int(from_to_w[1])]["in"].append(int(from_to_w[0]))
            weights[int(from_to_w[0])][int(from_to_w[1])] = int(from_to_w[2])

        answer = solve(src, dst, adj, weights)
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
            expected = (int(lines[0]), [int(i) for i in lines[1].split()])
            passed = answer == expected

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba5d.txt"
    rosalind_output = "rosalind_ba5d_output.txt"
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
