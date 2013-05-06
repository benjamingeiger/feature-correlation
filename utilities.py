from __future__ import print_function

import sys

def debug (*args, **kwargs):
    if "file" not in kwargs:
        kwargs["file"] = sys.stderr
    print("DEBUG:", *args, **kwargs)

def pagebreak (lines = 10):
    for i in range(lines):
        print()


## Code borrowed from http://code.activestate.com/recipes/66472/
#def frange(start, end=None, inc=None):
##    "A range function, that does accept float increments..."
#
#    if end == None:
#        end = start + 0.0
#        start = 0.0
#
#    if inc == None:
#        inc = 1.0
#
#    L = []
#    while 1:
#        next = start + len(L) * inc
#        if inc > 0 and next >= end:
#            break
#        elif inc < 0 and next <= end:
#            break
#        L.append(next)
#        
#    return L

def frange(start, end=None, inc=None):
    "A range generator that accepts float increments."

    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    cur = start
    while True:
        yield cur
        
        cur += inc

        if inc > 0 and cur > end:
            break
        elif inc < 0 and cur < end:
            break

