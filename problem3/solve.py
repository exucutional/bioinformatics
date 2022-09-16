import os

def solve(genome : str) -> (int):
    res = set()
    skew = 0
    minskew = 0
    for i in range(len(genome)):
        if genome[i] == 'G':
            skew += 1
        
        if genome[i] == 'C':
            skew -= 1
        
        if skew == minskew:
            res.add(i+1)

        if skew < minskew:
            minskew = skew
            res.clear()
            res.add(i+1)

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
            answer = solve(genome)
            expected = set([int(i) for i in fout.readline().split()])
            passed = answer == expected
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")
            
def solve_problem():
    rosalind_input = "rosalind_ba1f.txt"
    rosalind_output = "rosalind_ba1f_output.txt"
    with open(rosalind_input, "r") as fin, open(rosalind_output, "w") as fout:
        lines  = fin.readlines()
        genome = lines[0].strip()
        answer = solve(genome)
        fout.write(" ".join([str(i) for i in answer]))
    
    print("Done")

#test()
solve_problem()