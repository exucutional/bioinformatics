from audioop import mul
from calendar import leapdays
from collections import defaultdict
import os
import sys
import time

from argparse import ArgumentParser

sys.setrecursionlimit(2000)


def expand(peptides, spectrum, m):
    masses = []
    l = len(spectrum)
    spectrum_dict = dict()
    for i in range(l):
        for j in range(i+1, l):
            diff = spectrum[j]-spectrum[i]
            if 57 <= diff <= 200:
                spectrum_dict[diff] = spectrum_dict.get(diff, 0) + 1
    sorted_masses = sorted(spectrum_dict.items(), key= lambda a:a[1], reverse=True)
    masses = [str(p[0]) for p in sorted_masses]
    multi = [p[1] for p in sorted_masses]
    t = multi[m-1]
    for i in range(m, 1):
        if multi[i] < t:
            masses = masses[:i]
            break
    
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


def linear_score(peptide, spectrum):
    if len(peptide) == 0:
        return 0
    
    peptide_list = [int(p) for p in peptide.split('-')]
    linear_spectrum = linearspectrum(peptide_list)
    score = 0
    for key, value in linear_spectrum.items():
        v = spectrum.get(key, 0)
        if v >= value:
            score += value
        else:
            score += v
    return score


def cut(leaderboard, spectrum, n):
    l = len(leaderboard)
    linear_score_dict = {}
    for peptide in leaderboard:
        linear_score_dict[peptide] = score(peptide, spectrum)

    linear_sorted = sorted(linear_score_dict.items(), key = lambda a:a[1], reverse=True)
    leaderboard = [peptide[0] for peptide in linear_sorted]
    leaderboard_scores = [peptide[1] for peptide in linear_sorted]
    for i in range(n, l):
        if leaderboard_scores[i] < leaderboard_scores[n-1]:
            return leaderboard[:i]
    
    return leaderboard


def score(peptide, spectrum):
    if len(peptide) == 0:
        return 0
    
    petpide_list = [int(p) for p in peptide.split('-')]
    cyclo_spectrum = cyclospectrum(petpide_list)
    score = 0
    for key, value in cyclo_spectrum.items():
        v = spectrum.get(key, 0)
        if v >= value:
            score += value
        else:
            score += v

    return score



def solve(spectrum, m, n):
    leaderboard = {""}
    parent_mass_spectrum = max(spectrum)
    res = [""]
    best_score = 0
    spectrum_dict = get_dict_from_spectrum(spectrum)
    while len(leaderboard) > 0:
        leaderboard = expand(leaderboard, spectrum, m)
        peptides_to_delete = []
        for peptide in leaderboard:
            if mass(peptide) == parent_mass_spectrum:
                peptide_score = score(peptide, spectrum_dict)
                if peptide_score > best_score:
                    res = [peptide]
                    best_score = peptide_score
                #elif peptide_score == best_score:
                    #res.append(peptide)
            elif mass(peptide) > parent_mass_spectrum:
                peptides_to_delete.append(peptide)

        for peptide in peptides_to_delete:
            leaderboard.remove(peptide)

        leaderboard = cut(leaderboard, spectrum_dict, n)

    return res


def read_and_solve(input_file):
    with open(input_file, "r") as fin:
        lines  = fin.readlines()
        m = int(lines[0])
        n = int(lines[1])
        spectrum = [int(i) for i in lines[2].split()]
        answer = solve(spectrum, m, n)
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
            passed = len(answer) == len(expected)
            for e in expected:
                if answer.count(e) != expected.count(e):
                    passed = False
                    break

            if not passed:
                print(f"-> Test {i} failed. Time {int(end-start)}s\n   Expected {expected}\n   Got      {answer}")
            else:
                print(f"-> Test {i} passed. Time {int(end-start)}s")


def solve_problem():
    rosalind_input = "rosalind_ba4i.txt"
    rosalind_output = "rosalind_ba4i_output.txt"
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