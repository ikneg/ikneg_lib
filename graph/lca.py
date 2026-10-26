class LCA:
    def __init__(self, graph, root=0):
        self.n = len(graph)
        if not 0 <= root < self.n:
            raise ValueError("root must be a vertex of a nonempty tree")
        self.depth = [-1] * self.n
        parent = [-1] * self.n
        self.depth[root] = 0
        stack = [root]
        while stack:
            v = stack.pop()
            for to in graph[v]:
                if not 0 <= to < self.n:
                    raise IndexError("vertex out of range")
                if to == parent[v]:
                    continue
                if self.depth[to] != -1:
                    raise ValueError("graph must be a tree")
                parent[to] = v
                self.depth[to] = self.depth[v] + 1
                stack.append(to)
        if -1 in self.depth:
            raise ValueError("tree must be connected")
        self.up = [parent]
        for _ in range(1, self.n.bit_length()):
            prev = self.up[-1]
            self.up.append([prev[p] if p != -1 else -1 for p in prev])

    def _check_vertex(self, v):
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")

    def kth_ancestor(self, v, k):
        self._check_vertex(v)
        if k < 0:
            raise ValueError("k must be nonnegative")
        if k > self.depth[v]:
            return -1
        i = 0
        while k:
            if k & 1:
                v = self.up[i][v]
            k >>= 1
            i += 1
        return v

    def lca(self, a, b):
        self._check_vertex(a)
        self._check_vertex(b)
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        a = self.kth_ancestor(a, self.depth[a] - self.depth[b])
        if a == b:
            return a
        for ancestors in reversed(self.up):
            if ancestors[a] != ancestors[b]:
                a, b = ancestors[a], ancestors[b]
        return self.up[0][a]

    def distance(self, a, b):
        ancestor = self.lca(a, b)
        return self.depth[a] + self.depth[b] - 2 * self.depth[ancestor]
