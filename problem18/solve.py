from collections import defaultdict
import os
import sys
import time

from argparse import ArgumentParser

sys.setrecursionlimit(2000)


def expand(peptides):
    masses = ["57", "71", "87", "97", "99", "101", "103", "113", "114", "115", "128", "129", "131", "137", "147", "156", "163", "186"]
    peptides_expanded = set()
    for peptide in peptides:
        if peptide == "":
            for mass in masses:
                peptides_expanded.add(mass)
        else:
            for mass in masses:
                peptides_expanded.add(peptide+"-"+mass)
    
    return peptides_expanded


def mass(peptide):
    return sum([int(i) for i in peptide.split('-')])


def linearspectrum(peptide):
    prefixes = [0]
    for i in range(len(peptide)):
        prefixes.append(prefixes[i]+peptide[i])

    spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i+1, len(peptide)+1):
            spectrum.append(prefixes[j]-prefixes[i])
    
    spectrumDict = dict()
    for s in spectrum:
        spectrumDict[s] = spectrumDict.get(s, 0) + 1
    
    return spectrumDict


def cyclospectrum(peptide):
    prefixes = [0]
    for i in range(len(peptide)):
        prefixes.append(prefixes[i]+peptide[i])

    spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i+1, len(peptide)+1):
            spectrum.append(prefixes[j]-prefixes[i])
            if i > 0 and j < len(peptide):
                spectrum.append(prefixes[len(peptide)]+prefixes[i]-prefixes[j])
    
    spectrumDict = dict()
    for s in spectrum:
        spectrumDict[s] = spectrumDict.get(s, 0) + 1
    
    return spectrumDict



def get_dict_from_spectrum(spectrum):
    spectrumDict = dict()
    for s in spectrum:
        spectrumDict[s] = spectrumDict.get(s, 0) + 1
    
    return spectrumDict


def cycloconsistent(peptide, spectrum):
    return cyclospectrum([int(i) for i in peptide.split('-')]) == get_dict_from_spectrum(spectrum)


def consistent(peptide, spectrum):
    linear_spectrum = linearspectrum([int(i) for i in peptide.split('-')])
    spectrum_dict = get_dict_from_spectrum(spectrum)
    for key, value in linear_spectrum.items():
        if value > spectrum_dict.get(key, 0):
            return False

    return True


def solve(spectrum):
    peptides = set([""])
    parent_mass_spectrum = max(spectrum)
    res = []
    while len(peptides) > 0:
        peptides = expand(peptides)
        peptides_to_delete = []
        for peptide in peptides:
            if mass(peptide) == parent_mass_spectrum:
                if cycloconsistent(peptide, spectrum):
                    res.append(peptide)
                peptides_to_delete.append(peptide)
            elif not consistent(peptide, spectrum):
                peptides_to_delete.append(peptide)
        
        for peptide in peptides_to_delete:
            peptides.remove(peptide)

    return res


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        spectrum = [int(i) for i in lines[0].split()]
        answer = solve(spectrum)
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
            expected = fout.readlines()[0].split()
            passed = True
            for e in expected:
                if answer.count(e) != expected.count(e):
                    passed = False
                    break

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba4e.txt"
    rosalind_output = "rosalind_ba4e_output.txt"
    answer = read_and_solve(rosalind_input)
    with open(rosalind_output, "w") as fout:
        fout.write(" ".join(answer))
    
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