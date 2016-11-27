import random
import copy
import time
import itertools
import math


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
    while vertices:
        v = vertices[0]
        found = False
        chain, stack = [], [(v, [v])]
        while not found and stack:
            i, path = stack.pop(0)
            for j in range(n):
                if G[i][j] == 1 and j in vertices and j not in path:
                    if len(path) == k:
                        found = True
                        chain = path + [j]
                        break
                    stack.append((j, path + [j]))
        if chain:
            chains.append(chain)
            for l in chain:
                vertices.remove(l)
        else:
            vertices.remove(v)
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


G = generate_graph(100, 0.1)
k = 3
print('Greedy:')
t = time.time()
greedy_solution = greedy(G, k)
print(len(greedy_solution))
print('{0:e}'.format(time.time() - t))
print('Local search:')
t = time.time()
print(len(local_search(greedy_solution, G, k)))
print('{0:e}'.format(time.time() - t))
print('Simulated annealing:')
t = time.time()
print(len(simulated_annealing(greedy_solution, G, k, 0.5, 0.5)))
print('{0:e}'.format(time.time() - t))
