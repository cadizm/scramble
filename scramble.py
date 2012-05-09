#!/usr/bin/env python

import sys
import re
import copy

DEBUG = False

##
## TODO: Refactor to separate core solver from presentation of solution.
## Also, add JSON interface (or something similar )to make web-ready
## Add associated word point score to results? Or push to presentation?
##

#
# Graph indices
#
#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
#

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


ARR = { -1 : '&larr;',
        -5 : '&nwarr;',
        -4 : '&uarr;',
        -3 : '&nearr;',
         1 : '&rarr;',
         5 : '&searr;',
         4 : '&darr;',
         3 : '&swarr;' }


POINTS = {  'a' :  1, 'b' :  4, 'c' :  4, 'd' :  2, 'e' :  1, 'f' :  4, 'g' :  3,
            'h' :  3, 'i' :  1, 'j' : 10, 'k' :  5, 'l' :  2, 'm' :  4, 'n' :  2,
            'o' :  1, 'p' :  4, 'q' : 10, 'r' :  1, 's' :  1, 't' :  1, 'u' :  2,
            'v' :  5, 'w' :  4, 'x' :  8, 'y' :  3, 'z' : 10, }


class Color():
    'Representation of RGB color'
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '#{0}{1}{2}'.format(format(self.r, '02x'),
                format(self.g, '02x'), format(self.b, '02x'))


def colors(N):
    'Return length N list of colors with gradations from green to yellow to red'
    if N > 2:
        mid = N / 2
        step = 0xff / (N - 2)
    else:
        mid = 0
        step = 0

    C = [Color(0, 0, 0) for n in range(N)]
    C[mid] = Color(0xff, 0xff, 0)
    C[-1] = Color(0xff, 0, 0)
    C[0] = Color(0, 0x80, 0)

    prev = C[mid]
    for c in reversed(C[1:mid]):
        c.r = prev.r - step
        c.g = prev.g
        c.b = prev.b + step
        prev = c

    prev = C[mid]
    for c in C[mid + 1:-1]:
        c.r = prev.r
        c.g = prev.g - step
        c.b = prev.b
        prev = c

    return [str(c) for c in C]


class Vertex():
    'Representation of vertex in graph'
    def __init__(self, index, label, visited=False,
            adjacent_vertices=[], adjacent_vertex_indices=[]):
        self.index = index
        self.label = label
        self.visited = visited
        self.adjacent_vertices = adjacent_vertices
        self.adjacent_vertex_indices = adjacent_vertex_indices

    def __str__(self):
        return '{0} : [{1}] [{2}]'.format(self.label,
                ' '.join(v.label for v in self.adjacent_vertices),
                ' '.join(str(i) for i in self.adjacent_vertex_indices))


def dfs(u, min_len, W, D, S, L, R):
    'Depth first search; prunes deadends and processes valid words. R is output param'
    S.append(u.label)
    L.append(u.index)
    s = ''.join(S)
    if prune(s, W):
        u.visited = False
        S.pop()
        L.pop()
        return
    if len(s) >= min_len and s in D:
        process(S, L)
        R.append((''.join(S), copy.deepcopy(L)))
    # Mark as visited when rooted at u
    u.visited = True
    for v in u.adjacent_vertices:
        if not v.visited:
            dfs(v, min_len, W, D, S, L, R)
    # Unmark to visit u when rooted elsewhere
    u.visited = False
    S.pop()
    L.pop()


def prune(s, W):
    'Prune if prefix s not in corpus'
    prefix = '^{0}.*?$'.format(s)
    return not re.search(prefix, W, re.S|re.M)


def process(S, L):
    'Processing for valid words'
    if DEBUG:
        print >> sys.stderr, ''.join(S), L
    C = colors(len(L))
    print '<tr><td><ol>'
    for k in A.keys():  # [0-15]
        if k in L:
            i = L.index(k)  # grid position
            s = S[i]  # letter
            if i + 1 < len(L):
                print '<li style="background-color: {0}">{1} {2}</li>'.format(C[i], s, ARR[L[i + 1] - L[i]])
            else:  # last letter
                print '<li style="background-color: {0}">{1}</li>'.format(C[i], s)
        else:
            print '<li>{0}</li>'.format('&nbsp;')
    print '</ol></td><td><span class="word">{0}</span></td></tr>'.format(''.join(S))


def build_graph_path(S):
    'Build graph V and critical vertices P from input string S'
    V = [Vertex(k, S[k]) for k in sorted(A.keys())]
    for i, v in enumerate(V):
        v.adjacent_vertices = [V[j] for j in A[i]]
        v.adjacent_vertex_indices = [j for j in A[i]]
    return V


def solve(S, min_len, _W):
    'Find words in string S a la Scramble with Friends'
    def keep_word(word):
        for letter in word:
            if letter not in S:
                return False
        return True

    D = filter(keep_word, _W.split())
    W = '\n'.join(D)

    if DEBUG:
        print >> sys.stderr, 'W: {0}'.format(len(W))
        print >> sys.stderr, 'D: {0}'.format(len(D))

    print """<html>
    <head>
        <link href="scramble.css" rel="stylesheet" />
    </head>
    <body>
        <table>"""
    V = build_graph_path(S)
    R = []
    for v in V:
        dfs(v, min_len, W, D, [], [], R)
    print """        </table>
</body>
</html>"""
    return R


if __name__ == '__main__':
    # One-time read from disk
    _W = open('words_gte_6.txt', 'r').read()  # Corpus as one big string

    _S = 'desuerneptapfeuw'
    min_len = 6

    _R = solve(_S.lower(), min_len, _W)

    for r in _R:
        print >> sys.stderr, r
