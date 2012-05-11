#!/usr/bin/env python

import timeit
import random
import string
import scramble


_W = open('words_gte_6.txt', 'r').read()

def random_puzzle():
    return ''.join(random.sample(string.ascii_lowercase, 16))

if __name__ == '__main__':
    for i in [1, 10, 50, 100]:
        print '{0} sec, {1} iterations'.format(timeit.timeit(
                stmt='scramble.solve(random_puzzle(), _W)',
                setup='from __main__ import scramble, random_puzzle, _W',
                number=i), i)
