from __future__ import print_function

from sys import argv, stderr, exit

from getopt import getopt, GetoptError

import re

#import sklearn.datasets as Lds

from utilities import debug as debug_print
from utilities import frange

from data import read_data
from correlation import find_correlation


def debug_silence(string):
    pass


DEBUG = True
if DEBUG:
    debug = debug_print
else:
    debug = debug_silence


def print_help():
    """Print usage information."""

    print("Usage: python {} [options] [filename]".format(argv[0]),
            file=stderr)
    print(file=stderr)
    print("Options:", file=stderr)
    print("    -h, -?, --help:", file=stderr)
    print("        This message.", file=stderr)
    print("    -n, --print-names:", file=stderr)
    print("        Print feature names instead of numbers.", file=stderr)


def parse_options(argv):
    """Parse command line options and arguments."""

    try:
        opts, args = getopt(argv[1:], "?hn", ["help", "print-names"])
    except GetoptError:
        print_help()
        exit(1)

    input_file_name = ""
    print_names = False

    for opt, arg in opts:
        if opt in ["-h", "-?", "--help"]:
            print_help()
            exit(1)
        if opt in ["-n", "--print-names"]:
            print_names = True

    if len(args) == 1:
        input_file_name = args[0]
    elif len(args) > 1:
        print_help()
        exit(2)

    return input_file_name, print_names


#NOTE: This is brittle. I'll work on making it robust later.
def relieff(results, instances, neighbors=10, samplesize=-1, sigma=2):

    # Set up the lists for neighbor finding.
    classes = set(int(round(r)) for r in results)

    if len(results) != len(instances):
        raise Exception("Number of results != number of instances.")

    elements = {}
    for c in classes:
        elements[c] = []

    for i in len(instances):
        elements[results[int(round(results[i]))]].append(results[i])

    for c in classes:
        elements[c].sort()


def parse_relieff_list(filetext):
    fileparts = [re.split(" +", x.strip(), maxsplit=2) for x in filetext]

    return [(float(x[0]), int(x[1]) - 1, x[2]) for x in fileparts]


def select_features(features, relieff_features, correlations, threshold=0.9):
    selected = [relieff_features[0][1]]
    index = 1
    #while len(selected) < 10 and index < features.shape[1]:
    while index < features.shape[1]:
        current = relieff_features[index][1]
        #debug("Selection:", selected)
        debug("Trying", current, "...")
        add = True
        for x in selected:
            a = min(x, current)
            b = max(x, current)
            corr = correlations[(a, b)][0]
            if abs(corr) > threshold:
                debug("(collides with", x, ")")
                add = False
        if add:
            selected.append(current)
        index += 1

    return selected


def main():
    relieff_file = open("/home/bgeiger/Dropbox/Research/Features/Relief-F ranking 46.txt", "r")
    relieff_features = parse_relieff_list(relieff_file.readlines())
    relieff_features.sort(key=lambda x: x[0], reverse=True)

    name, print_names = parse_options(argv)
    results, features, feature_names = read_data(name)

    #features = np.hstack((features, results.reshape((len(results), 1))))

    correlations = find_correlation(features)
    #print("\n".join("{}: {}".format(x, correlations[x]) for x in correlations))
    #return

    for threshold in frange(1.0, 0.0, -0.1):
        selected = select_features(features, relieff_features, correlations, threshold)

        print("============================================================")
        print("THRESHOLD =", threshold)
        print("Count:", len(selected))
        print("\n".join(["{} ({})".format(x, feature_names[x]) for x in selected]))

        print()
        print()
        print()


if __name__ == "__main__":
    main()
