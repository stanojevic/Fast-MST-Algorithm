
__author__ = "Miloš Stanojević"
__license__ = "Apache-2.0"


import numpy as np

class EdgePriorityQueue:

    def __init__(self, node_id: int, edge_weights: np.ndarray):
        self.target = np.full(edge_weights.shape, node_id)
        self.weights = edge_weights
        self.weights[node_id] = np.nan

    def __len__(self):
        return np.count_nonzero(~np.isnan(self.weights))

    def extract_max(self) -> (int, int, float):
        i = np.nanargmax(self.weights)
        if np.isnan(self.weights[i]):  # nanargmax bug with -inf
            i = np.argmax(np.isinf(self.weights))
        w = self.weights[i]
        self.weights[i] = np.nan
        return i, self.target[i], w

    def meld_inplace(self, other) -> None:
        to_replace = (self.weights < other.weights)
        self.target[to_replace] = other.target[to_replace]
        self.weights[to_replace] = other.weights[to_replace]
        self.weights[np.isnan(other.weights)] = np.nan

    def add_const(self, const: float):
        self.weights[~np.isinf(self.weights)] += const


def tarjan(weights : np.ndarray) -> np.ndarray:
    weights = weights.copy()  # just in case
    weights[:, 0] = -np.inf
    n = weights.shape[0]
    max_vertices = n*2-1
    vertices_in = [None for _ in range(max_vertices)]
    vertices_prev = np.zeros(max_vertices, dtype=int)-1
    vertices_children = [[] for _ in range(max_vertices)]
    vertices_queues = [EdgePriorityQueue(dep, weights[:, dep]) for dep in range(n)] + [None for _ in range(max_vertices-n)]
    vertices_parent = np.arange(max_vertices)
    vertices_highway = np.arange(max_vertices)
    next_free = n

    ######### compression phase ########
    a = n-1
    while len(vertices_queues[a]) != 0:
        u, v, w = vertices_queues[a].extract_max()
        b = vertices_highway[u]  # find
        assert a != b, "there should be no self-loop in this implementation"
        vertices_in[a] = (u, v, w)
        vertices_prev[a] = b
        if vertices_in[u] is None:
            # path extended
            a = b
        else:
            # new cycle formed, collapse
            c = next_free
            next_free += 1

            i = a
            while True:
                i = vertices_highway[i]  # find
                vertices_children[c].append(i)
                i = vertices_prev[i]
                if vertices_highway[i] == a:  # find
                    break

            for i in vertices_children[c]:
                vertices_parent[i] = c
                vertices_highway[vertices_highway == vertices_highway[i]] = c  # union by collapsing
                vertices_queues[i].add_const(-vertices_in[i][2])
                if vertices_queues[c] is None:
                    vertices_queues[c] = vertices_queues[i]
                else:
                    vertices_queues[c].meld_inplace(vertices_queues[i])
            a = c

    ######### expansion phase ########
    R = []

    def dismantle(u: int):
        while vertices_parent[u] != u:
            for v in vertices_children[vertices_parent[u]]:
                if v == u:
                    continue
                vertices_parent[v] = v
                if vertices_children[v] != []:
                    R.append(v)
            u = vertices_parent[u]

    dismantle(0)
    while R != []:
        c = R.pop()
        u, v, w = vertices_in[c]
        vertices_in[v] = (u, v, w)
        dismantle(v)
    output = np.zeros(n, dtype=int)-1
    for u in range(1, n):
        output[u] = vertices_in[u][0]
    return output


def is_tree(proposal: np.array) -> bool:
    n = proposal.shape[0]
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[proposal[i]].append(i)
    is_visited = np.zeros(n, dtype=bool)
    stack = [0]
    while len(stack) != 0:
        i = stack.pop()
        is_visited[i] = True
        stack.extend(children[i])
    return is_visited.all()


def reweighting(weights: np.array):
    weights_no_inf = np.where(np.isinf(weights), np.nan, weights)
    weights = weights.copy()
    n = weights.shape[0]-1
    correction = n*(np.nanmax(weights_no_inf)-np.nanmin(weights_no_inf))+1
    weights[0] -= correction
    weights[0, 0] = -np.inf
    return weights


# weights[head][dep] =  weight of head ---> dep (head entering dep)
def fast_parse(weights: np.array, one_root: bool) -> np.array:
    proposal = weights.argmax(axis=1)
    root_count = np.count_nonzero(proposal[1:] == 0)

    if is_tree(proposal) and (not one_root or root_count == 1):
        result = proposal
    else:
        if one_root:
            weights = reweighting(weights)
        result = tarjan(weights)
    result[0] = -1
    return result
