import os

def solve(pattern : str, genome : str) -> [int]:
    i = genome.find(pattern, 0)
    res = []
    while i != -1:
        res.append(i)
        i = genome.find(pattern, i + 1)
    
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
            answer = solve(pattern, genome)
            expected = fout.readline().split()
            passed = True
            if len(answer) == len(expected):
                for j in range(len(answer)):
                    if answer[j] != int(expected[j]):
                        passed = False
                        break
            else:
                passed = False
            
            if not passed:
                print(f"-> Test {i} failed\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed")
            
def solve_problem():
    rosalind_input = "rosalind_ba1d.txt"
    rosalind_output = "rosalind_ba1d_output.txt"
    with open(rosalind_input, "r") as fin, open(rosalind_output, "w") as fout:
        lines = fin.readlines()
        pattern = lines[0].strip()
        genome = lines[1].strip()
        answer = solve(pattern, genome)
        fout.write(" ".join([str(i) for i in answer]))
    
    print("Done")

solve_problem()