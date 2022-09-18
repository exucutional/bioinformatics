import os
from collections import defaultdict


def hamming_distance(str1, str2):
    res = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            res += 1
    return res


def complement(kmer : str) -> str:
    reverse = list(kmer[::-1])
    for i in range(len(reverse)):
        if reverse[i] == 'A':
            reverse[i] = 'T'
        elif reverse[i] == 'T':
            reverse[i] = 'A'
        elif reverse[i] == 'G':
            reverse[i] = 'C'
        elif reverse[i] == 'C':
            reverse[i] = 'G'

    return "".join(reverse)


def get_neighbours(kmer : str, d : int) -> (str):
    if d == 0:
        return (kmer,)
    
    if len(kmer) == 1:
        return set(["A", "C", "T", "G"])

    neighbours = set()
    suffix = kmer[1:]
    suffix_neighbours = get_neighbours(suffix, d)
    for neighbour in suffix_neighbours:
        if hamming_distance(suffix, neighbour) < d:
            for x in ("A", "C", "T", "G"):
                neighbours.add(x + neighbour)
        else:
            neighbours.add(kmer[0] + neighbour)
    
    return neighbours


def solve(genome : str, k : int, d : int) -> (str):
    res = set()
    neighbours = defaultdict(int)
    for i in range(len(genome)-k+1):
        for kmer in get_neighbours(genome[i:i+k], d):
            neighbours[kmer] += 1

        for kmer in get_neighbours(complement(genome[i:i+k]), d):
            neighbours[kmer] += 1

    max_count = 0
    for kmer, count in neighbours.items():
        if count > max_count:
            max_count = count
            res.clear()
            res.add(kmer)
        
        if count == max_count:
            res.add(kmer)

    return res


def read_and_solve(input_file : str) -> (str):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        genome = lines[0].strip()
        args = lines[1].strip().split()
        k = int(args[0])
        d = int(args[1])
        answer = solve(genome, k, d)
        return answer


def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    for i in range(1, files_n + 1):
        answer = read_and_solve(os.path.join(input_dir, f"input_{i}.txt"))
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            expected = set(fout.readline().split())
            passed = answer == expected
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")


def solve_problem():
    rosalind_input = "rosalind_ba1j.txt"
    rosalind_output = "rosalind_ba1j_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(" ".join([str(i) for i in answer]))
    
    print("Done")


#test()
solve_problem()