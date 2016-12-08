import random
import copy
import time
import itertools
import math
from itertools import combinations


def generate_graph(n, p):
    G = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = G[j][i] = 1
    return G

def rebuild(path, full):
    print "Path " + str(path)
    full_old = copy.deepcopy(full)

    full[path[0]] = [path[1]]
    full[path[1]] = [path[0], path[2]]
    full[path[2]] = [path[1]]

    for i in xrange(len(path[3:-1])):
        l = path[i-1]
        v = path[i]
        r = path[i+1]
        if set([l, r]) == set(full_old[v]):
            next = path[i+2]
            full[r] = [v, next]
            full[next] = [r]
            full[v] = [r]
            continue
        if len(full_old[v]) == 2:
            up = set(full[v]) - set([l, r])
            full[v] = [up, r]
            full[r] = [v]



def find_path(G, v, path, full, flag):
    if flag[0]:
        return
    if full[v] and len(full[v]) == 1 and full[v][1] != path[-2]:
        path.append(full[v][1])
        find_path(G, full[v][1], path, flag)
        return
    if full[v] and len(full[v]) == 1:
        for to in xrange(len(G)):
            if G[v][to] == 1:
                if not full[to]:
                    path.append(to)
                    flag[0] = True
                    return
                path.append(to)
                find_path(G, to, path, flag)
                if flag[0]:
                    return
                path = path[:-1]
        return 
    if full[v] and len(full[v]) == 2:
        for to in xrange(len(G)):
            if G[v][to] == 1 and to != path[-2]:
                if not full[to]:
                    path.append(to)
                    flag[0] = True
                    return
                path.append(to)
                find_path(G, to, path, flag)
                if flag[0]:
                    return
                path = path[:-1]
        return
    
def Kun3(G):
    n = len(G)
    full = [None for x in xrange(n)] # pair, 1 elem, or None
    vertices = list(xrange(n))
    
    for v in xrange(n):
        print "V + "+ str(v) + " Full + " + str(full)
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G [pair[1]][v] == 1 and not full[pair[0]] and not full[pair[1]]:
                full[pair[0]] = [v]
                full[pair[1]] = [v]
                full[v] = [pair[0], pair[1]]
                break
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G[pair[1]][v] == 1 and full[pair[0]] and not full[pair[1]]:
                path = [pair[1], v, pair[0]]
                find_path(G, pair[0], path, full, [False])
                rebuild(path, full)
                break
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G[pair[1]][v] == 1 and not full[pair[0]] and full[pair[1]]:
                path = [pair[0], v, pair[1]]
                find_path(G, pair[1], path, full, [False])
                rebuild(path, full)
                break

    solution = []
    for v in xrange(n):
        if full[v] != None and len(full[v]) == 2:
            solution.append([v] + full[v])
    return solution

random.seed(12345)
G = generate_graph(10, 0.5)
print G
#G = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
s = Kun3(G)
print s
    