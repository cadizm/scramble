#!/usr/bin/env python

#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
#

import re

# Adjacency list for graph
A = { 0 : [ 1,  4,  5],
      1 : [ 0,  2,  4,  5,  6],
      2 : [ 1,  3,  5,  6,  7],
      3 : [ 2,  6,  7], 
      4 : [ 0,  1,  5,  8,  9],
      5 : [ 0,  1,  2,  4,  6,  8,  9, 10],
      6 : [ 1,  2,  3,  5,  7,  9, 10, 11],
      7 : [ 2,  3,  6, 10, 11],
      8 : [ 4,  5,  9, 12, 13],
      9 : [ 4,  5,  6,  8, 10, 12, 13, 14],
     10 : [ 5,  6,  7,  9, 11, 13, 14, 15],
     11 : [ 6,  7, 10, 14, 15],
     12 : [ 8,  9, 13],
     13 : [ 8,  9, 10, 12, 14],
     14 : [ 9, 10, 11, 13, 15],
     15 : [10, 11, 14] }

# Corpus as one big string
W = open('words.txt', 'r').read()

# Corpus as an array of strings
D = W.split()


class Vertex:
    'Representation of vertex in graph'
    def __init__(self, index, label, visited=False, adjacent_vertices=[]):
        self.index = index
        self.label = label
        self.visited = visited
        self.adjacent_vertices = adjacent_vertices

    def __str__(self):
        return '{0} : [{1}]'.format(self.label,
                ' '.join(v.label for v in self.adjacent_vertices))


def dfs(u, S, L):
    'Depth first search; prunes deadends and processes valid words'
    S.append(u.label)
    L.append(u.index)
    s = ''.join(S)
    if prune(s):
        u.visited = False
        S.pop()
        L.pop()
        return
    if s in D:
        process(s, L)
    u.visited = True
    for v in u.adjacent_vertices:
        if not v.visited:
            dfs(v, S, L)
    u.visited = False
    S.pop()
    L.pop()


def process(s, L):
    'Processing for valid words'
    print s, ' '.join(str(i) for i in L)


def prune(s):
    'Return False if prefix s in corpus'
    prefix = '^{0}.*?$'.format(s)
    return not re.search(prefix, W, re.S|re.M)


def build_graph(S):
    'Build graph from input string S and adjacency list A'
    V = [Vertex(k, S[k]) for k in sorted(A.keys())]
    for i, v in enumerate(V):
        v.adjacent_vertices = [V[j] for j in A[i]]
    return V


def solve(S):
    'Find words in string S a la Scramble with Friends'
    for v in build_graph(S):
        dfs(v, [], [])


if __name__ == '__main__':
    solve('skdmnetrnisacpdy'.lower())
