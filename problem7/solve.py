import os

from numpy import Inf

p = 4 # pceudo


def calc_prob(kmer, profile):
    assert(len(kmer) == len(profile[0]))
    prob = 1
    for i in range(len(kmer)):
        offset = {
            'A': 0,
            'C': 1,
            'G': 2,
            'T': 3,
        }
        prob *= profile[offset[kmer[i]]][i]
    
    return prob


def form_profile(motifs):
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
            profile[offset[motifs[j][i]]][i] += 1
        
        for j in range(len(profile)):
            profile[j][i] += p
            profile[j][i] /= len(motifs) + p

    return profile


def form_most_probable(dna, profile):
    most_prob = ""
    max_prob = 0
    k = len(profile[0])
    for i in range(len(dna)-k+1):
        kmer = dna[i:i+k]
        prob = calc_prob(kmer, profile)
        if prob > max_prob:
            max_prob = prob
            most_prob = kmer

    return most_prob


def calc_score(motifs):
    score = 0
    offset = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3,
    }
    for i in range(len(motifs[0])):
        count = [p]*4
        for j in range(len(motifs)):
            count[offset[motifs[j][i]]] += 1
        
        score += len(motifs) + p - max(count)
    
    return score




def solve(dna, k, t):
    best_motifs = []
    for i in range(len(dna)):
        best_motifs.append(dna[i][0:0+k])

    best_score = calc_score(best_motifs)
    for i in range(len(dna[0])-k+1):
        motifs = [dna[0][i:i+k]]

        for j in range(1, len(dna)):
            profile = form_profile(motifs)
            motifs.append(form_most_probable(dna[j], profile))

        score = calc_score(motifs)
        if score < best_score:
            best_score = score
            best_motifs = motifs[:]


    return best_motifs


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        args = lines[0].strip().split()
        k = int(args[0])
        t = int(args[1])
        dna = lines[1].strip().split()
        answer = solve(dna, k, t)
        return answer


def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    for i in range(1, files_n + 1):
        answer = read_and_solve(os.path.join(input_dir, f"input_{i}.txt"))
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            expected = fout.readline().strip().split()
            passed = answer == expected
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")


def solve_problem():
    rosalind_input = "rosalind_ba2e.txt"
    rosalind_output = "rosalind_ba2e_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(" ".join(answer))
    
    print("Done")


#test()
solve_problem()
