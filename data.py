from __future__ import print_function

from sys import stdin

from math import isnan

import numpy as np
import scipy as sp

from utilities import debug as debug_print


def debug_silence(string):
    pass


DEBUG = True
if DEBUG:
    debug = debug_print
else:
    debug = debug_silence


def read_data(input_file_name, get_feature_names=True):
    """Pull data from the specified file."""
    if input_file_name != "":
        input_file = open(input_file_name, "r")
    else:
        input_file = stdin

    feature_names = input_file.readline()[:-1].split(",")
    data = sp.genfromtxt(input_file, delimiter=",", skip_header=0)
    data, true_results = np.hsplit(data, (-1,))
    true_results = true_results.transpose()[0]

    if isnan(true_results[0]):
        data = data[1:]
        true_results = true_results[1:]

    return true_results, data, feature_names


def main():
    pass

if __name__ == "__main__":
    main()
