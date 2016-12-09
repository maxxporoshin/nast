import random
import copy
import time
import itertools
import math
from itertools import combinations
#from graph_tool.all import *


def generate_graph(n, p):
    G = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = G[j][i] = 1
    return G
path = []
full = []
used = []
flag = False

def rebuild():
    global path, full, used, flag
    print "rebuild" + str(path)
    full_old = copy.deepcopy(full)

    full[path[0]] = [path[1]]
    full[path[1]] = [path[0], path[2]]
    full[path[2]] = [path[1]]

    for i in xrange(3, len(path[:-1])):
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



def find_path(G, v):
    global path, full, used, flag
    if flag:
        return
    if full[v] and len(full[v]) == 1 and full[v][0] != path[-2]:
        path.append(full[v][0])
        used[full[v][0]] = True
        find_path(G, full[v][0])
        if not flag:
            used[full[v][0]] = False
            path = path[:-1]
        return
    if full[v] and len(full[v]) == 1:
        for to in xrange(len(G)):
            if G[v][to] == 1 and not used[to]:
                if not full[to]:
                    path.append(to)
                    flag = True
                    return
                path.append(to)
                used[to] = True
                find_path(G, to)
                if flag:
                    return
                path = path[:-1]
                used[to] = False
        return
    if full[v] and len(full[v]) == 2 and path[-2] in full[v]:
        for to in xrange(len(G)):
            if G[v][to] == 1 and to != path[-2] and not used[to]:
                if not full[to]:
                    path.append(to)
                    flag[0] = True
                    return
                path.append(to)
                used[to] = True
                find_path(G, to)
                if flag:
                    return
                used[to] = False
                path = path[:-1]
        return


def Kun3(G):
    global path, full, used, flag
    n = len(G)
    full = [None for x in xrange(n)] # pair, 1 elem, or None
    vertices = list(xrange(n))

    for v in xrange(n):
        print "V + "+ str(v) + " Full + " + str(full)
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G[pair[1]][v] == 1 and not full[pair[0]] and not full[pair[1]]:
                full[pair[0]] = [v]
                full[pair[1]] = [v]
                full[v] = [pair[0], pair[1]]
                break
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G[pair[1]][v] == 1 and full[pair[0]] and not full[pair[1]]:
                path = [pair[1], v, pair[0]]
                used = [False] * n
                used[pair[1]] = True
                used[v] = True
                used[pair[0]] = True
                flag = False
                find_path(G, pair[0])
                rebuild()
                break
        if full[v]:
            continue
        for pair in combinations(vertices, 2):
            if G[v][pair[0]] == 1 and G[pair[1]][v] == 1 and not full[pair[0]] and full[pair[1]]:
                path = [pair[0], v, pair[1]]
                used = [False] * n
                used[pair[1]] = True
                used[v] = True
                used[pair[0]] = True
                flag = False
                find_path(G, pair[1])
                rebuild()
                break

    solution = []
    for v in xrange(n):
        if full[v] != None and len(full[v]) == 2:
            solution.append([v] + full[v])
    return solution


"""

g = Graph()
g.add_vertex()
graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18,
           output_size=(200, 200), output="two-nodes.png")
"""

random.seed(12345)
G = generate_graph(10, 0.5)
print G
#G = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
s = Kun3(G)
print s
