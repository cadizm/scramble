#!/usr/bin/env python

import sys
import re
import copy
import json
import memcache

DEBUG = True

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


# Letter to point mapping
POINTS = {  'a' :  1, 'b' :  4, 'c' :  4, 'd' :  2, 'e' :  1, 'f' :  4,
            'g' :  3, 'h' :  3, 'i' :  1, 'j' : 10, 'k' :  5, 'l' :  2,
            'm' :  4, 'n' :  2, 'o' :  1, 'p' :  4, 'q' : 10, 'r' :  1,
            's' :  1, 't' :  1, 'u' :  2, 'v' :  5, 'w' :  4, 'x' :  8,
            'y' :  3, 'z' : 10, }


class Vertex():
    'Representation of vertex in graph'
    def __init__(self, index, label, visited=False, adjacent_vertices=[]):
        self.index = index
        self.label = label
        self.visited = visited
        self.adjacent_vertices = adjacent_vertices

    def __str__(self):
        return '{0} : [{1}]'.format(self.label,
                ' '.join(v.label for v in self.adjacent_vertices))


def dfs(u, min_len, W, D, S, L, R):
    """Depth first search rooted at u, with dead end pruning.

    DFS started at graph rooted at vertex u. W and D contain valid the valid
    word corpuses and should not be modified. S and L are used for bookkeeping
    and should also not be modified. Solution is returned via output param R,
    containing words found with length >= min_len"""
    S.append(u.label)
    L.append(u.index)
    s = ''.join(S)
    if prune(s, W):
        u.visited = False
        S.pop()
        L.pop()
        return
    if len(s) >= min_len and s in D:
        R.append([''.join(S), copy.deepcopy(L)])
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


def build_graph_path(S):
    'Build graph V and critical vertices P from input string S'
    V = [Vertex(k, S[k]) for k in sorted(A.keys())]
    for i, v in enumerate(V):
        v.adjacent_vertices = [V[j] for j in A[i]]
    return V


def order(R):
    """Returned R ordered by descending score

    Score ranked by sum of points assigned to each letter.
    Higher rank is given to words of length >= 8"""
    for i, r in enumerate(R):
        word, indices = r
        length, score = len(word), sum(map(lambda x: POINTS[x], word))
        R[i] = (length, score, word, indices)
    def rank(x, y):
        length_x, length_y = x[0], y[0]
        score_x, score_y = x[1], y[1]
        if length_x == length_y:
            return cmp(score_y, score_x)
        elif score_x == score_y:
            return cmp(length_y, length_x)
        else:
            if max(length_x, length_y) < 8:
                return cmp(score_y, score_x)
            else:
                return cmp(length_y, length_x)
    return sorted(R, rank)


def solve(S, _W, min_len=6, fmt=None):
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
    V = build_graph_path(S)
    R = []
    for v in V:
        dfs(v, min_len, W, D, [], [], R)
    if fmt == 'json':
        return json.dumps([{'word': r[2], 'indices': r[3]} for r in order(R)],
                separators=(',',':'))
    else:
        return order(R)


if __name__ == '__main__':
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    _W1 = mc.get('_W1')
    _W2 = mc.get('_W2')
    if not _W1 or not _W1:
        _W1 = open('words_gte_6-1.txt', 'r').read()
        _W2 = open('words_gte_6-2.txt', 'r').read()
        if not mc.set('_W1', _W1) or not mc.set('_W2', _W2):
            print 'Error: couldnt set dictionary'
            sys.exit()
    _W = _W1 + _W2
    _S = 'lawimetkeneouasl'
    _R = mc.get(_S)
    if not _R:
        _R = solve(_S.lower(), _W)
        mc.set(_S, _R)
    if DEBUG:
        for r in _R:
            print >> sys.stderr, r
