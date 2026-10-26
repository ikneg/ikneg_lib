class UnionFind:
    def __init__(self, n):
        if n < 0:
            raise ValueError("n must be nonnegative")
        self.n = n
        self.parent = [-1] * n
        self.group_count = n

    def leader(self, a):
        if not 0 <= a < self.n:
            raise IndexError("vertex out of range")
        root = a
        while self.parent[root] >= 0:
            root = self.parent[root]
        while a != root:
            self.parent[a], a = root, self.parent[a]
        return root

    def merge(self, a, b):
        a, b = self.leader(a), self.leader(b)
        if a == b:
            return a
        if self.parent[a] > self.parent[b]:
            a, b = b, a
        self.parent[a] += self.parent[b]
        self.parent[b] = a
        self.group_count -= 1
        return a

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def size(self, a):
        return -self.parent[self.leader(a)]

    def groups(self):
        result = {}
        for a in range(self.n):
            result.setdefault(self.leader(a), []).append(a)
        return list(result.values())
