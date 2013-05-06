from __future__ import print_function

from sys import argv

import networkx as nx

import numpy as N

import correlation
import utilities


def main():
    name, fmt = correlation.parse_options(argv)
    results, features, feature_names = correlation.read_data(name, fmt)

    features = N.hstack((features, results.reshape((len(results), 1))))

    correlations = correlation.find_correlation(features)

    g = nx.Graph()

    #g.add_nodes_from(range(len(results) + 1))

    threshold = 0.8

    for (f1, f2) in [c for c in correlations.keys() if correlations[c][0] > threshold]:
        g.add_edge(f1, f2)

    cliques = sorted(nx.find_cliques(g), key=len, reverse=True)
    cliques = [c for c in cliques if len(c) >= 3]

    print("=====CLIQUES=====")
    for clique in cliques:
        print()
        print("Clique, length:", len(clique))
        for node in sorted(clique):
            print("{:>3} ({})".format(node, feature_names[node]))

    print()
    print()
    print("=====CLIQUE COUNT=====")
    print()
    cliquecount = {}
    for clique in cliques:
        for node in clique:
            cliquecount[node] = cliquecount.get(node, 0) + 1
    cliquesizelist = [(c, cliquecount[c]) for c in sorted(cliquecount, key=lambda x: (cliquecount.get(x), -1 * x), reverse=True)]
    for c in cliquesizelist: print("{:>3}: {:>3} ({})".format(c[1], c[0], feature_names[c[0]]))




if __name__ == "__main__":
    main()
