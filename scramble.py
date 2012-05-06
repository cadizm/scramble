#!/usr/bin/env python

#
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
W = open('words1.txt', 'r').read()

# Corpus as an array of strings
D = W.split()

ARR = { -1 : '&larr;',
        -5 : '&nwarr;',
        -4 : '&uarr;',
        -3 : '&nearr;',
         1 : '&rarr;',
         5 : '&searr;',
         4 : '&darr;',
         3 : '&swarr;' }

FLAGS = { 'tr': 0
        }


class Vertex:
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


def dfs(u, S, L, min_len):
    'Depth first search; prunes deadends and processes valid words'
    S.append(u.label)
    L.append(u.index)
    s = ''.join(S)
    if prune(s):
        u.visited = False
        S.pop()
        L.pop()
        return
    if len(s) >= min_len and s in D:
        process(S, L)
    # Mark as visited when rooted at u
    u.visited = True
    for v in u.adjacent_vertices:
        if not v.visited:
            dfs(v, S, L, min_len)
    # Unmark to visit u when rooted elsewhere
    u.visited = False
    S.pop()
    L.pop()


def process(S, L):
    'Processing for valid words'
    if FLAGS['tr'] == 0:
        print '<tr>'
    FLAGS['tr'] += 1
    print '<td><ol>'
    for k in A.keys():
        if k in L:
            i = L.index(k)
            c = S[i]
            if i + 1 < len(L):
                if i == 0:
                    print '<li style="background-color: #00FF00">{0} {1}</li>'.format(c, ARR[L[i + 1] - L[i]])
                else:
                    print '<li>{0} {1}</li>'.format(c, ARR[L[i + 1] - L[i]])
            else:
                print '<li>{0} {1}</li>'.format(c, '&#8226;')
        else:
                print '<li>{0}</li>'.format('&nbsp;')
    print '</ol></td>'
    if FLAGS['tr'] == 3:
        print '</tr>'
        FLAGS['tr'] = 0


def prune(s):
    'Prune if prefix s not in corpus'
    prefix = '^{0}.*?$'.format(s)
    return not re.search(prefix, W, re.S|re.M)


def build_graph_path(S):
    'Build graph V and critical vertices P from input string S'
    V = [Vertex(k, S[k]) for k in sorted(A.keys())]
    for i, v in enumerate(V):
        v.adjacent_vertices = [V[j] for j in A[i]]
        v.adjacent_vertex_indices = [j for j in A[i]]
    P = []
    for v in V:
        if v.index in Z:
            P.extend(v.adjacent_vertex_indices)
    return set(P), V


def solve(S, Z, min_len):
    'Find words in string S a la Scramble with Friends'
    print """<html>
    <head>
        <link href="scramble.css" rel="stylesheet" />
    </head>
    <body>
        <table>"""
    P, V = build_graph_path(S)
    for v in V:
#        if v.index in Z:
        if v.index in P:
            dfs(v, [], [], min_len)
    print """        </table>
</body>
</html>"""


if __name__ == '__main__':
    min_len = 6
#    Z = [8, 11, 12, 15]  # `Critical-path indices'
#    Z = [11, 12, 15]  # `Critical-path indices'
    Z = [8]  # `Critical-path indices'
    solve('desuerneptapfeuw'.lower(), Z, min_len)
