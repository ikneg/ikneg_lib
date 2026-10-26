import math
import random
import runpy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    return runpy.run_path(str(ROOT / path))[name]


UnionFind = load("data_structures/union_find.py", "UnionFind")
coordinate_compress = load("data_structures/coordinate_compression.py", "coordinate_compress")
LCA = load("graph/lca.py", "LCA")
SCC = load("graph/scc.py", "SCC")
MaxFlow = load("graph/max_flow.py", "MaxFlow")
RollingHash = load("string/rolling_hash.py", "RollingHash")
Combination = load("math/combination.py", "Combination")
binomial_coefficients = load("math/combination.py", "binomial_coefficients")
mod_inverse = load("math/mod_inverse.py", "mod_inverse")


class AdditionalAlgorithmsTest(unittest.TestCase):
    def test_union_find(self):
        rng = random.Random(10)
        for n in (1, 2, 17):
            uf = UnionFind(n)
            labels = list(range(n))
            for _ in range(100):
                a, b = rng.randrange(n), rng.randrange(n)
                old, new = labels[b], labels[a]
                labels = [new if label == old else label for label in labels]
                root = uf.merge(a, b)
                self.assertEqual(root, uf.leader(a))
                self.assertEqual(uf.group_count, len(set(labels)))
                for i in range(n):
                    self.assertEqual(uf.size(i), labels.count(labels[i]))
                    for j in range(n):
                        self.assertEqual(uf.same(i, j), labels[i] == labels[j])
            self.assertEqual(sorted(v for g in uf.groups() for v in g), list(range(n)))
        self.assertEqual(UnionFind(0).groups(), [])
        self.assertEqual(UnionFind(0).group_count, 0)
        with self.assertRaises(IndexError):
            UnionFind(2).leader(-1)
        with self.assertRaises(ValueError):
            UnionFind(-1)

    def test_coordinate_compression(self):
        for values in ([], [5], [40, -3, 40, 10**30, 0], ["b", "a", "b"]):
            compressed, originals = coordinate_compress(iter(values))
            self.assertEqual([originals[i] for i in compressed], values)
            self.assertEqual(originals, sorted(set(values)))
            for i, a in enumerate(values):
                for j, b in enumerate(values):
                    self.assertEqual(a < b, compressed[i] < compressed[j])

    def test_lca(self):
        rng = random.Random(11)
        for n in (1, 2, 7, 40):
            graph = [[] for _ in range(n)]
            for v in range(1, n):
                p = rng.randrange(v)
                graph[p].append(v)
                graph[v].append(p)
            for root in {0, n - 1}:
                parent = [-1] * n
                depth = [-1] * n
                depth[root] = 0
                queue = [root]
                for v in queue:
                    for to in graph[v]:
                        if depth[to] == -1:
                            parent[to] = v
                            depth[to] = depth[v] + 1
                            queue.append(to)
                tree = LCA(graph, root)
                self.assertEqual(tree.depth, depth)
                for a in range(n):
                    v = a
                    for k in range(depth[a] + 2):
                        self.assertEqual(tree.kth_ancestor(a, k), v)
                        if v != -1:
                            v = parent[v]
                    for b in range(n):
                        x, y = a, b
                        while depth[x] > depth[y]:
                            x = parent[x]
                        while depth[y] > depth[x]:
                            y = parent[y]
                        while x != y:
                            x, y = parent[x], parent[y]
                        self.assertEqual(tree.lca(a, b), x)
                        self.assertEqual(tree.distance(a, b), depth[a] + depth[b] - 2 * depth[x])
        with self.assertRaises(ValueError):
            LCA([[], []])
        with self.assertRaises(ValueError):
            LCA([[1, 2], [0, 2], [0, 1]])
        with self.assertRaises(ValueError):
            LCA([])
        with self.assertRaises(ValueError):
            LCA([[]]).kth_ancestor(0, -1)
        with self.assertRaises(IndexError):
            LCA([[]]).lca(-1, 0)

    def test_rolling_hash(self):
        rng = random.Random(12)
        for text in ("", "a", "abracadabra", "あいうあいう", "\0a\0", "".join(rng.choices("abc", k=50))):
            hashed = RollingHash(text)
            for l in range(len(text) + 1):
                for r in range(l, len(text) + 1):
                    other = RollingHash(text[l:r])
                    self.assertEqual(hashed.get(l, r), other.get(0, r - l))
                    expected = 0
                    for char in text[l:r]:
                        expected = (expected * hashed.base + ord(char) + 1) % ((1 << 61) - 1)
                    self.assertEqual(hashed.get(l, r), expected)
        self.assertEqual(RollingHash("abc").base, RollingHash("def").base)
        self.assertEqual(RollingHash("abc", 257).get(0, 3), RollingHash("abc", 257).get(0, 3))
        with self.assertRaises(IndexError):
            RollingHash("abc").get(-1, 2)
        with self.assertRaises(ValueError):
            RollingHash("abc", 1)

    def test_scc_against_reachability(self):
        rng = random.Random(13)
        for n in range(9):
            for _ in range(20):
                graph = SCC(n)
                reach = [[a == b for b in range(n)] for a in range(n)]
                for a in range(n):
                    for b in range(n):
                        if rng.random() < 0.2:
                            graph.add_edge(a, b)
                            graph.add_edge(a, b)
                            reach[a][b] = True
                for k in range(n):
                    for a in range(n):
                        for b in range(n):
                            reach[a][b] |= reach[a][k] and reach[k][b]
                groups = graph.scc()
                self.assertEqual(groups, graph.scc())
                self.assertEqual(sorted(v for g in groups for v in g), list(range(n)))
                ids = [0] * n
                for i, group in enumerate(groups):
                    for v in group:
                        ids[v] = i
                for a in range(n):
                    for b in range(n):
                        self.assertEqual(ids[a] == ids[b], reach[a][b] and reach[b][a])
                    for b in graph.graph[a]:
                        self.assertLessEqual(ids[a], ids[b])
        graph = SCC(2)
        graph.add_edge(0, 1)
        self.assertEqual(graph.scc(), [[0], [1]])
        graph.add_edge(1, 0)
        self.assertEqual(len(graph.scc()), 1)

    def test_combination_and_binomial_theorem(self):
        for mod in (101, 998244353, 10**9 + 7):
            combination = Combination(40, mod)
            for n in range(41):
                coefficients = binomial_coefficients(n)
                self.assertEqual(coefficients, [math.comb(n, r) for r in range(n + 1)])
                for r in range(-1, n + 2):
                    expected = math.comb(n, r) % mod if 0 <= r <= n else 0
                    self.assertEqual(combination.comb(n, r), expected)
                self.assertEqual(sum(c * 2**(n - r) * (-3)**r
                                     for r, c in enumerate(coefficients)), (2 - 3)**n)
        self.assertEqual(Combination(0).comb(0, 0), 1)
        self.assertEqual(Combination(2, 9).comb(2, 1), 2)
        for args in ((-1, 7), (3, 3), (3, 6), (0, 1)):
            with self.assertRaises(ValueError):
                Combination(*args)
        with self.assertRaises(ValueError):
            Combination(3).comb(4, 2)
        with self.assertRaises(ValueError):
            binomial_coefficients(-1)

    def test_mod_inverse(self):
        for mod in range(2, 60):
            for a in range(-60, 61):
                if math.gcd(a, mod) == 1:
                    inv = mod_inverse(a, mod)
                    self.assertTrue(0 <= inv < mod)
                    self.assertEqual(a * inv % mod, 1)
                else:
                    with self.assertRaises(ValueError):
                        mod_inverse(a, mod)
        for mod in (0, 1, -7):
            with self.assertRaises(ValueError):
                mod_inverse(3, mod)

    def test_max_flow_against_exhaustive_cuts(self):
        rng = random.Random(14)
        for n in range(2, 8):
            for _ in range(40):
                graph = MaxFlow(n)
                original = []
                for _ in range(n * n):
                    source, target = rng.randrange(n), rng.randrange(n)
                    capacity = rng.randrange(8)
                    i = graph.add_edge(source, target, capacity)
                    original.append((source, target, capacity))
                    self.assertEqual(graph.get_edge(i), (source, target, capacity, 0))
                expected = min(
                    sum(c for a, b, c in original if mask >> a & 1 and not mask >> b & 1)
                    for mask in range(1 << n) if mask & 1 and not mask >> (n - 1) & 1
                )
                limit = rng.randrange(6)
                first = graph.flow(0, n - 1, limit)
                self.assertEqual(first, min(expected, limit))
                self.assertEqual(first + graph.flow(0, n - 1), expected)
                self.assertEqual(graph.flow(0, n - 1), 0)
                cut = graph.min_cut(0)
                self.assertTrue(cut[0])
                self.assertFalse(cut[-1])
                self.assertEqual(sum(c for a, b, c in original if cut[a] and not cut[b]), expected)
                balance = [0] * n
                for (a, b, capacity), edge in zip(original, graph.edges()):
                    self.assertEqual(edge[:3], (a, b, capacity))
                    flow = edge[3]
                    self.assertTrue(0 <= flow <= capacity)
                    balance[a] -= flow
                    balance[b] += flow
                self.assertEqual(balance, [-expected] + [0] * (n - 2) + [expected])

    def test_max_flow_boundaries(self):
        graph = MaxFlow(2)
        graph.add_edge(0, 0, 17)
        graph.add_edge(0, 1, 10**40)
        self.assertEqual(graph.flow(0, 1, 0), 0)
        self.assertEqual(graph.flow(0, 1), 10**40)
        graph.add_edge(0, 1, 3)
        self.assertEqual(graph.flow(0, 1), 3)
        with self.assertRaises(ValueError):
            graph.flow(0, 0)
        with self.assertRaises(ValueError):
            graph.add_edge(0, 1, -1)
        with self.assertRaises(ValueError):
            graph.flow(0, 1, -1)
        with self.assertRaises(IndexError):
            graph.add_edge(-1, 0, 1)

    def test_deep_graphs(self):
        n = 3000
        tree = [[] for _ in range(n)]
        scc = SCC(n)
        flow = MaxFlow(n)
        for v in range(n - 1):
            tree[v].append(v + 1)
            tree[v + 1].append(v)
            scc.add_edge(v, v + 1)
            flow.add_edge(v, v + 1, 1)
        self.assertEqual(LCA(tree).distance(0, n - 1), n - 1)
        self.assertEqual(scc.scc(), [[v] for v in range(n)])
        self.assertEqual(flow.flow(0, n - 1), 1)


if __name__ == "__main__":
    unittest.main()
