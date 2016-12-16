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


def greedy(G, k, vertices=[]):
    n = len(G)
    if not vertices:
        vertices = list(range(n))
    chains = []
    vertices_to_try = vertices[:]
    while vertices_to_try:
        v = vertices_to_try[0]
        found = False
        chain, stack = [], [(v, [v])]
        while not found and stack:
            i, path = stack.pop()
            for j in range(n):
                if G[i][j] == 1 and j in vertices and j not in path:
                    if len(path) == k - 1:
                        found = True
                        chain = path + [j]
                        break
                    stack.append((j, path + [j]))
        if chain:
            chains.append(chain)
            for l in chain:
                vertices.remove(l)
                if l in vertices_to_try:
                    vertices_to_try.remove(l)
        else:
            vertices_to_try.remove(v)
    return chains


def local_search(S, G, k):
    solution = copy.deepcopy(S)
    iterations = 0
    more_chains = True
    while more_chains:
        more_chains = False
        for i in range(len(solution)):
            T = copy.deepcopy(solution)
            T.pop(i)
            vertices = set(range(len(G)))
            for chain in T:
                vertices = vertices - set(chain)
            new_chains = greedy(G, k, list(vertices))
            if len(new_chains) > 1:
                solution = T + new_chains
                more_chains = True
                break
        iterations += 1
    print('Iterations: ' + str(iterations))
    return solution


def simulated_annealing(S, G, k, p1, p2):
        solution = copy.deepcopy(S)
        iterations = 0
        more_chains = True
        while more_chains:
            more_chains = False
            for i in range(len(solution)):
                T = copy.deepcopy(solution)
                T.pop(i)
                vertices = set(range(len(G)))
                for chain in T:
                    vertices = vertices - set(chain)
                new_chains = greedy(G, k, list(vertices))
                if len(new_chains) > 1 or random.random() < math.exp(-p1 * iterations):
                    solution = T + new_chains
                    more_chains = True
                    break
            if not more_chains:
                subsets = itertools.combinations(range(len(solution)), 2)
                for subset in subsets:
                    T = copy.deepcopy(solution)
                    T.pop(subset[1])
                    T.pop(subset[0])
                    vertices = set(range(len(G)))
                    for chain in T:
                        vertices = vertices - set(chain)
                    new_chains = greedy(G, k, list(vertices))
                    if len(new_chains) > 2 or random.random() < math.exp(-p2 * iterations):
                        solution = T + new_chains
                        more_chains = True
                        break
            iterations += 1
        print('Iterations: ' + str(iterations))
        return solution


path = []
full = []
used = []
flag = False

def rebuild():
    global path, full, used, flag
    full_old = copy.deepcopy(full)

    full[path[0]] = [path[1]]
    full[path[1]] = [path[0], path[2]]
    full[path[2]] = [path[1]]

    for i in xrange(3, len(path[:-1])):
        l = path[i-1]
        v = path[i]
        r = path[i+1]
        #print ([l,r])
        #print(full_old[v])
        if set([l, r]) == set(full_old[v]):
            next = path[i+2]
            full[r] = [v, next]
            full[next] = [r]
            full[v] = [r]
            continue
        if len(full_old[v]) == 2:
            up = list(set(full_old[v]) - set([l, r]))[0]
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
                    flag = True
                    return
                path.append(to)
                used[to] = True
                find_path(G, to)
                if flag:
                    return
                used[to] = False
                path = path[:-1]
        return


def Kun3(G, iter = 1):
    global path, full, used, flag
    n = len(G)
    full = [None for x in xrange(n)] # pair, 1 elem, or None
    vertices = list(xrange(n))
    vert = list(xrange(n))
    random.shuffle(vert)
    for _ in xrange(iter):
        for v in vert:
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

def clear_all():
    path = []
    full = []
    used = []
    flag = False

"""
for _ in xrange(100):
    r = random.randint(1, 10000)
    clear_all()
    random.seed(r)
    G = generate_graph(100, 0.1)
    k = 3
    #print('Greedy:')
    t = time.time()
    greedy_solution = greedy(G, k)
    #print(greedy_solution)
    #print('Total {}'.format(len(greedy_solution)))
    #print('{0:e}'.format(time.time() - t))

    kun3 = Kun3(G)
    #print('Total {}'.format(len(kun3)))

    print('Total {} vs {}'.format(len(greedy_solution), len(kun3)))
"""

for _ in xrange(100):
    r = random.randint(1, 10000)
    clear_all()
    random.seed(r)
    G = generate_graph(500, 0.1)

    t = time.time()
    kun3_1 = Kun3(G, 1)
    #print(greedy_solution)
    #print('Total {}'.format(len(greedy_solution)))
    print('{0:e}'.format(time.time() - t))

    kun3_3 = Kun3(G, 2)
    #print('Total {}'.format(len(kun3)))
    #if len(kun3_3) > len(kun3_1):
    print('Total {} vs {}'.format(len(kun3_3), len(kun3_1)))

"""
print('Local search:')
t = time.time()
print(len(local_search(greedy_solution, G, k)))
print('{0:e}'.format(time.time() - t))
print('Simulated annealing:')
t = time.time()
print(len(simulated_annealing(greedy_solution, G, k, 0.5, 0.5)))
print('{0:e}'.format(time.time() - t))
"""
