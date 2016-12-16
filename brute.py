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
from itertools import combinations

def brut(G, central, free):
    if len(central) == 0:
        return []
    v = central[0]
    solutions = []
    for pair in combinations(free, 2):

        left_free = [x for x in free if x not in pair]

        if G[pair[0]][v] == 1 and G[v][pair[1]] == 1:
            solution = brut(G, central[1:], left_free)
            if solution is not None:
                solution.append([v, pair[0], pair[1]])
                solutions.append(solution)
    if len(solutions) == 0:
        return None
    answer = solutions[0]
    for solution in solutions:
        if len(answer) < len(solution):
            answer = solution
    return answer

def check_is_solution(G, vertices, m):
    if m == 0:
        return []
    for central in combinations(vertices, m):
        free = [x for x in vertices if x not in central]
        solution = brut(G, central, free)
        if solution and len(solution) >= m:
            return solution
    return None



def brute3(G):
    n = len(G)
    l = 0
    r = n / 3
    vertices = list(range(n))

    while r - l > 1:
        m = (r + l) / 2
        is_solution = check_is_solution(G, vertices, m)
        if is_solution is not None:
            l = m
        else:
            r = m
    solution = check_is_solution(G, vertices, r)
    if solution is not None:
        return solution
    return check_is_solution(G, vertices, l)


G = generate_graph(20, 0.1)
k = 3
#print('Greedy:')
t = time.time()
brute3_solution = brute3(G)
#print(greedy_solution)
#print('Total {}'.format(len(greedy_solution)))
#print('{0:e}'.format(time.time() - t))

print('Total {}, int time {}'.format(len(brute3_solution), time.time() - t))