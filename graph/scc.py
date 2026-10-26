class SCC:
    def __init__(self, n):
        if n < 0:
            raise ValueError("n must be nonnegative")
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.reverse_graph = [[] for _ in range(n)]

    def add_edge(self, source, target):
        if not (0 <= source < self.n and 0 <= target < self.n):
            raise IndexError("vertex out of range")
        self.graph[source].append(target)
        self.reverse_graph[target].append(source)

    def scc(self):
        visited = [False] * self.n
        order = []
        for start in range(self.n):
            if visited[start]:
                continue
            visited[start] = True
            stack = [(start, 0)]
            while stack:
                v, i = stack[-1]
                if i == len(self.graph[v]):
                    order.append(v)
                    stack.pop()
                    continue
                stack[-1] = (v, i + 1)
                to = self.graph[v][i]
                if not visited[to]:
                    visited[to] = True
                    stack.append((to, 0))
        visited = [False] * self.n
        groups = []
        for start in reversed(order):
            if visited[start]:
                continue
            visited[start] = True
            stack = [start]
            group = []
            while stack:
                v = stack.pop()
                group.append(v)
                for to in self.reverse_graph[v]:
                    if not visited[to]:
                        visited[to] = True
                        stack.append(to)
            groups.append(group)
        return groups
