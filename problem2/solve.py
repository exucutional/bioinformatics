import os
from collections import defaultdict

def solve(genome : str, k : int, L : int, t : int) -> (str):
    #print(genome, k, L, t)
    gmap = defaultdict(int)
    l = 0
    r = 0
    res = set()
    while r < len(genome):
        if r - l > L - 1:
            gmap[genome[l:l+k]] -= 1
            l += 1

        if r - l + 1 >= k:
            kmer = genome[r-k+1:r+1]
            gmap[kmer] += 1
            if gmap[kmer] >= t and kmer not in res:
                res.add(kmer)

        #if gmap["CCA"] >= t:
            #print(genome[l:r + 1], genome[l:l+k], genome[r-k+1:r+1], gmap)
    
        r += 1

    return res

def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    for i in range(1, files_n + 1):
        with open(os.path.join(input_dir, f"input_{i}.txt"), "r") as fin,\
            open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout: 
            lines  = fin.readlines()
            genome = lines[0].strip()
            params = lines[1].strip().split()
            k = int(params[0])
            L = int(params[1])
            t = int(params[2])
            answer = solve(genome, k, L, t)
            expected = set(fout.readline().strip().split())
            passed = answer == expected
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")
            
def solve_problem():
    rosalind_input = "rosalind_ba1e.txt"
    rosalind_output = "rosalind_ba1e_output.txt"
    with open(rosalind_input, "r") as fin, open(rosalind_output, "w") as fout:
        lines  = fin.readlines()
        genome = lines[0].strip()
        params = lines[1].strip().split()
        k = int(params[0])
        L = int(params[1])
        t = int(params[2])
        answer = solve(genome, k, L, t)
        fout.write(" ".join(answer))
    
    print("Done")

#test()
solve_problem()