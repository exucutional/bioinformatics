import os

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


def solve(genome, k, profile):
    res = ""
    maxprob = 0
    for i in range(len(genome)-k+1):
        kmer = genome[i:i+k]
        prob = calc_prob(kmer, profile)
        if prob > maxprob:
            maxprob = prob
            res = kmer

    return res


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        genome = lines[0].strip()
        k = int(lines[1].strip())
        profile = []
        for i in range(4):
            profile.append([float(i) for i in lines[i+2].strip().split()])

        answer = solve(genome, k, profile)
        return answer


def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    for i in range(1, files_n + 1):
        answer = read_and_solve(os.path.join(input_dir, f"input_{i}.txt"))
        with open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout:
            expected = fout.readline().strip()
            passed = answer == expected
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")


def solve_problem():
    rosalind_input = "rosalind_ba2c.txt"
    rosalind_output = "rosalind_ba2c_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(answer)
    
    print("Done")


#test()
solve_problem()
