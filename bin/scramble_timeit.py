#!/usr/bin/env python

import os
import timeit
import random
import string
from scramble import solver

_dir = os.path.dirname(__file__)
_dir = os.path.join('..', 'scramble', 'scramble', 'data')
_dir = os.path.realpath(_dir)

_P = { 0 : solver.Constants.TL,
       6 : solver.Constants.TL,
      10 : solver.Constants.TL,
      14 : solver.Constants.TW }

_W = open('%s/words.txt' % _dir, 'r').read()

def random_puzzle():
    return ''.join(random.sample(string.ascii_lowercase, 16))

if __name__ == '__main__':
    for i in [1, 10, 50, 100]:
        print '{0} sec, {1} iterations'.format(timeit.timeit(
                stmt='solver.solve(random_puzzle(), _P, _W)',
                setup='from __main__ import solver, random_puzzle, _P, _W',
                number=i), i)
