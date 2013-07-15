from __future__ import print_function

from sys import argv, stderr, exit

from getopt import getopt, GetoptError

import numpy as np
import scipy.stats as sps

#import sklearn.datasets as Lds

from utilities import debug as debug_print

from data import read_data


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


def find_correlation(features):
    num_features = features.shape[1]

    correlation = {}

    for i in range(num_features):
        left_features = features[:, i]
        for j in range(i + 1, num_features):
            right_features = features[:, j]

            corr, p = sps.pearsonr(left_features, right_features)

            correlation[(i, j)] = (corr, p)

    return correlation


def main():
    name, print_names = parse_options(argv)
    results, features, feature_names = read_data(name)

    features = np.hstack((features, results.reshape((len(results), 1))))

    correlation = find_correlation(features)

    correlationorder = sorted(correlation,
                              key=lambda x: abs(correlation.get(x)[0]),
                              reverse=True)

    #print("Feature numbers")
    #print()
    #print("number\tname")
    #print("------\t----")
    #for i in range(len(feature_names)):
        #print("{}\t{}".format(i, feature_names[i]))

    #print()
    #print()
    #print("Correlations")
    #print()
    #print("ft1\tft2\tpearson")
    #print("---\t---\t-------")
    #for c in correlationorder:
        #print("{}\t{}\t{}".format(c[0], c[1], correlation[c][0]))

    for c in correlationorder:
        if print_names:
            print('"{}","{}",{}'.format(feature_names[c[0]],
                                        feature_names[c[1]],
                                        correlation[c][0]))
        else:
            print('{},{},{}'.format(c[0],
                                    c[1],
                                    correlation[c][0]))


if __name__ == "__main__":
    main()
