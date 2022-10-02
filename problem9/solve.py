import os
import random
import time
from numpy import Inf

p = 4 # pceudo

def calc_prob(kmer, profile):
    prob = 1
    offset = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3,
    }
    for i in range(len(kmer)):
        prob *= profile[offset[kmer[i]]][i]
    
    return prob


def form_profile(motifs, r):
    profile = [[], [], [], []]
    offset = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3,
    }
    for i in range(len(motifs[0])):
        for j in range(len(profile)):
            profile[j].append(0)

        for j in range(len(motifs)):
            if j != r:
                profile[offset[motifs[j][i]]][i] += 1
        
        for j in range(len(profile)):
            profile[j][i] += 1
            profile[j][i] /= len(motifs) - 1 + p

    return profile


def form_random_probable(dna, profile):
    probs = []
    kmers = []
    k = len(profile[0])
    for i in range(len(dna)-k+1):
        kmer = dna[i:i+k]
        prob = calc_prob(kmer, profile)
        probs.append(prob)
        kmers.append(kmer)

    return random.choices(kmers, weights=probs, k=1)[0]


def calc_score(motifs):
    score = 0
    offset = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3,
    }
    for i in range(len(motifs[0])):
        count = [0]*4
        for j in range(len(motifs)):
            count[offset[motifs[j][i]]] += 1
        
        score += len(motifs)-max(count)
    
    return score


def random_solve(dna, k, t, N):
    best_motifs = []
    for i in range(len(dna)):
        pos = random.sample(range(0, len(dna[i])-k+1), 1)[0]
        best_motifs.append(dna[i][pos:pos+k])

    best_score = calc_score(best_motifs)
    motifs = best_motifs[:]
    for i in range(N):
        r = random.sample(range(0, t), 1)[0]
        profile = form_profile(motifs, r)
        motifs[r] = form_random_probable(dna[r], profile)

        score = calc_score(motifs)
        if score < best_score:
            best_score = score
            best_motifs = motifs[:]

    return (best_motifs, best_score)


def solve(dna, k, t, N):
    random.seed(time.time())
    best_motifs, best_score = random_solve(dna, k, t, N)
    for _ in range(20):
        motifs, score = random_solve(dna, k, t, N)
        if score < best_score:
            best_motifs = motifs[:]
            best_score = score
    
    return best_motifs


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        args = lines[0].strip().split()
        k = int(args[0])
        t = int(args[1])
        N = int(args[2])
        dna = lines[1].strip().split()
        answer = solve(dna, k, t, N)
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
            expected = fout.readline().strip().split()
            passed = answer == expected
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba2g.txt"
    rosalind_output = "rosalind_ba2g_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write("\n".join(answer))
    
    print("Done")


#test()
solve_problem()
