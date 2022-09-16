import os

def hamming_distance(str1, str2):
    res = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            res += 1
    return res

def solve(pattern : str, genome : str, d : int) -> (int):
    res = set()
    for i in range(len(genome)-len(pattern)+1):
        if hamming_distance(pattern, genome[i:i+len(pattern)]) <= d:
            res.add(i)
    
    return res

def test():
    input_dir = "inputs"
    output_dir = "outputs"

    files_n = len(os.listdir(input_dir))

    for i in range(1, files_n + 1):
        with open(os.path.join(input_dir, f"input_{i}.txt"), "r") as fin,\
            open(os.path.join(output_dir, f"output_{i}.txt"), "r") as fout: 
            lines  = fin.readlines()
            pattern = lines[0].strip()
            genome = lines[1].strip()
            if len(genome) < len(pattern):
                tmp = pattern
                pattern = genome
                genome = tmp

            d = int(lines[2].strip())
            answer = solve(pattern, genome, d)
            expected = set([int(i) for i in fout.readline().split()])
            passed = answer == expected
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")
            
def solve_problem():
    rosalind_input = "rosalind_ba1h.txt"
    rosalind_output = "rosalind_ba1h_output.txt"
    with open(rosalind_input, "r") as fin, open(rosalind_output, "w") as fout:
        lines  = fin.readlines()
        pattern = lines[0].strip()
        genome = lines[1].strip()
        if len(genome) < len(pattern):
            tmp = pattern
            pattern = genome
            genome = tmp

        d = int(lines[2].strip())
        answer = solve(pattern, genome, d)
        fout.write(" ".join([str(i) for i in answer]))
    
    print("Done")

#test()
solve_problem()