import os
import time

def hamming_distance(str1, str2):
    assert(len(str1) == len(str2))
    res = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            res += 1
    return res


def solve(pattern, dna):
    k = len(pattern)
    distance = 0
    for s in dna:
        minhamdist = float("inf")
        for i in range(len(s)-k+1):
            hamdist = hamming_distance(pattern, s[i:i+k])
            if hamdist < minhamdist:
                minhamdist = hamdist
        
        distance += minhamdist
    
    return distance


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        pattern = lines[0].strip()
        dna = lines[1].strip().split()
        answer = solve(pattern, dna)
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
            expected = fout.readline().strip()
            passed = answer == int(expected)
            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba2h.txt"
    rosalind_output = "rosalind_ba2h_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(str(answer))
    
    print("Done")


#test()
solve_problem()
