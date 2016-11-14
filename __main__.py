import random


def generate_graph(n, p):
    G = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                G[i][j] = G[j][i] = 1
    return G


def greedy(G, k):
    n = len(G)
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


G = generate_graph(10, 0.6)
print(greedy(G, 3))
