from __future__ import print_function

from sys import argv, stderr, exit

from getopt import getopt, GetoptError

import re

#import sklearn.datasets as Lds

from utilities import debug as debug_print
from utilities import frange

from data import read_data
from correlation import find_correlation


def debug_silence(*args, **kwargs):
    pass


DEBUG = True
if DEBUG:
    debug = debug_print
else:
    debug = debug_silence




FEATURE_FILENAME = "/home/bgeiger/Dropbox/Research/Features/LIDC_features_33_cases_46_features_normalized_-1to1.fixed.csv"

RELIEFF_FILENAME = "/home/bgeiger/Dropbox/Research/Features/Relief-F ranking 46.txt"



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
    relieff_file = open(RELIEFF_FILENAME, "r")
    relieff_features = parse_relieff_list(relieff_file.readlines())
    relieff_features.sort(key=lambda x: x[0], reverse=True)

    results, features, feature_names = read_data(FEATURE_FILENAME)

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
