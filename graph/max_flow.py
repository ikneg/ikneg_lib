from collections import deque


class MaxFlow:
    def __init__(self, n):
        if n < 0:
            raise ValueError("n must be nonnegative")
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.positions = []

    def _check_vertex(self, v):
        if not 0 <= v < self.n:
            raise IndexError("vertex out of range")

    def add_edge(self, source, target, capacity):
        self._check_vertex(source)
        self._check_vertex(target)
        if not isinstance(capacity, int) or capacity < 0:
            raise ValueError("capacity must be a nonnegative integer")
        forward = len(self.graph[source])
        backward = len(self.graph[target]) + (source == target)
        self.positions.append((source, forward))
        self.graph[source].append([target, backward, capacity])
        self.graph[target].append([source, forward, 0])
        return len(self.positions) - 1

    def get_edge(self, i):
        if not 0 <= i < len(self.positions):
            raise IndexError("edge out of range")
        source, index = self.positions[i]
        target, reverse, residual = self.graph[source][index]
        flow = self.graph[target][reverse][2]
        return source, target, residual + flow, flow

    def edges(self):
        return [self.get_edge(i) for i in range(len(self.positions))]

    def flow(self, source, sink, limit=None):
        self._check_vertex(source)
        self._check_vertex(sink)
        if source == sink:
            raise ValueError("source and sink must differ")
        if limit is None:
            limit = sum(edge[2] for edge in self.graph[source])
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a nonnegative integer")
        total = 0
        while total < limit:
            level = [-1] * self.n
            level[source] = 0
            queue = deque([source])
            while queue:
                v = queue.popleft()
                for to, _, capacity in self.graph[v]:
                    if capacity > 0 and level[to] == -1:
                        level[to] = level[v] + 1
                        queue.append(to)
            if level[sink] == -1:
                break
            current = [0] * self.n
            while total < limit:
                vertices = [source]
                path = []
                amounts = [limit - total]
                while vertices and vertices[-1] != sink:
                    v = vertices[-1]
                    while current[v] < len(self.graph[v]):
                        edge = self.graph[v][current[v]]
                        if edge[2] > 0 and level[edge[0]] == level[v] + 1:
                            break
                        current[v] += 1
                    if current[v] == len(self.graph[v]):
                        level[v] = -1
                        vertices.pop()
                        amounts.pop()
                        if path:
                            parent, _ = path.pop()
                            current[parent] += 1
                    else:
                        to, _, capacity = self.graph[v][current[v]]
                        path.append((v, current[v]))
                        vertices.append(to)
                        amounts.append(min(amounts[-1], capacity))
                if not vertices:
                    break
                amount = amounts[-1]
                for v, index in path:
                    edge = self.graph[v][index]
                    edge[2] -= amount
                    self.graph[edge[0]][edge[1]][2] += amount
                total += amount
        return total

    def min_cut(self, source):
        self._check_vertex(source)
        reached = [False] * self.n
        reached[source] = True
        stack = [source]
        while stack:
            v = stack.pop()
            for to, _, capacity in self.graph[v]:
                if capacity > 0 and not reached[to]:
                    reached[to] = True
                    stack.append(to)
        return reached
