import random
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path, name):
    return runpy.run_path(str(ROOT / path))[name]


class LibraryTest(unittest.TestCase):
    def test_shortest_paths(self):
        dijkstra = load("graph/dijkstra.py", "dijkstra")
        bfs = load("graph/zero_one_bfs.py", "zeroOneBFS")
        rng = random.Random(0)
        for _ in range(40):
            n = 8
            graph = [[(j, rng.randrange(2)) for j in range(n)
                      if rng.random() < 0.2] for _ in range(n)]
            expected = [10**18] * n
            expected[0] = 0
            for _ in range(n - 1):
                for v in range(n):
                    for nxt, cost in graph[v]:
                        expected[nxt] = min(expected[nxt], expected[v] + cost)
            self.assertEqual(dijkstra(graph, 0), expected)
            self.assertEqual(bfs(graph, 0), expected)
        self.assertEqual(dijkstra([[(1, 9), (2, 2)], [], [(1, 3)], []], 0),
                         [0, 5, 2, 10**18])

    def test_data_structures(self):
        bit = load("data_structures/bit.py", "BIT")(7)
        tree = load("data_structures/rmq.py", "rmq")(7)
        values = [0] * 7
        rng = random.Random(1)
        for _ in range(50):
            i = rng.randrange(7)
            delta = rng.randrange(-10**13, 10**13)
            values[i] += delta
            bit.add(i + 1, delta)
            tree.update(i + 1, values[i])
            for l in range(7):
                for r in range(l + 1, 8):
                    self.assertEqual(bit.sum(r) - bit.sum(l), sum(values[l:r]))
                    self.assertEqual(tree.query(l + 1, r + 1), max(values[l:r]))
        self.assertEqual(tree.query(2, 2), float("-inf"))
        self.assertEqual(tree.query(1, 8, 1, tree.siz + 1, 1), max(values))
        bit.length(7)
        self.assertEqual(bit.sum(7), 0)

    def test_integer_division(self):
        ceil = load("math/ceil.py", "ceil")
        floor = load("math/floor.py", "floor")
        from fractions import Fraction
        import math
        for a in range(-10, 11):
            for b in range(-5, 6):
                if b:
                    self.assertEqual(ceil(a, b), math.ceil(Fraction(a, b)))
                    self.assertEqual(floor(a, b), math.floor(Fraction(a, b)))
