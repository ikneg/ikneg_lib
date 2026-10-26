import random
import runpy
import unittest
from pathlib import Path


LazySegmentTree = runpy.run_path(str(
    Path(__file__).resolve().parents[1] / "data_structures/lazy_segtree.py"
))["LazySegmentTree"]


def affine_tree(values):
    return LazySegmentTree(
        [(x, 1) for x in values],
        op=lambda x, y: (x[0] + y[0], x[1] + y[1]),
        e=(0, 0),
        mapping=lambda f, x: (f[0] * x[0] + f[1] * x[1], x[1]),
        composition=lambda f, g: (f[0] * g[0], f[0] * g[1] + f[1]),
        id_=(1, 0),
    )


class LazySegmentTreeTest(unittest.TestCase):
    def test_random_operations(self):
        rng = random.Random(42)
        for n in (0, 1, 2, 3, 7, 8, 9, 31, 32, 33):
            values = [rng.randrange(-20, 21) for _ in range(n)]
            tree = affine_tree(values)
            for _ in range(200):
                l, r = sorted((rng.randrange(n + 1), rng.randrange(n + 1)))
                kind = rng.randrange(5)
                if kind <= 2:
                    a = (1, 0, rng.randrange(-2, 3))[kind]
                    b = rng.randrange(-10, 11)
                    tree.apply(l, r, (a, b))
                    for i in range(l, r):
                        values[i] = a * values[i] + b
                elif kind == 3 and n:
                    p = rng.randrange(n)
                    values[p] = rng.randrange(-100, 101)
                    tree.set(p, (values[p], 1))
                self.assertEqual(tree.prod(l, r), (sum(values[l:r]), r - l))
                self.assertEqual(tree.all_prod(), (sum(values), n))
                if n:
                    p = rng.randrange(n)
                    self.assertEqual(tree.get(p), (values[p], 1))
            for l in range(n + 1):
                for r in range(l, n + 1):
                    self.assertEqual(tree.prod(l, r), (sum(values[l:r]), r - l))

    def test_pending_updates_and_composition_order(self):
        tree = affine_tree(range(8))
        tree.apply(0, 8, (0, 5))
        tree.apply(0, 8, (1, 3))
        tree.apply(0, 8, (2, 1))
        self.assertEqual(tree.all_prod(), (136, 8))
        self.assertEqual(tree.get(3), (17, 1))
        tree.set(4, (0, 1))
        tree.apply(2, 7, (0, 0))
        self.assertEqual([tree.get(i)[0] for i in range(8)],
                         [17, 17, 0, 0, 0, 0, 0, 17])
        self.assertEqual(tree.all_prod(), (51, 8))

    def test_readme_addition_example(self):
        tree = LazySegmentTree(
            [(x, 1) for x in [1, 2, 3, 4, 5]],
            op=lambda a, b: (a[0] + b[0], a[1] + b[1]),
            e=(0, 0),
            mapping=lambda f, x: (x[0] + f * x[1], x[1]),
            composition=lambda f, g: f + g,
            id_=0,
        )
        tree.apply(1, 4, 10)
        self.assertEqual(tree.prod(1, 4)[0], 39)
        self.assertEqual(tree.all_prod()[0], 45)
        self.assertEqual(tree.get(2)[0], 13)
        tree.set(2, (7, 1))
        self.assertEqual(tree.prod(0, 3)[0], 20)

    def test_assignment_and_noncommutative_aggregation(self):
        tree = LazySegmentTree(
            iter("abcdefg"), op=lambda a, b: a + b, e="",
            mapping=lambda f, x: x if f is None else f * len(x),
            composition=lambda f, g: g if f is None else f, id_=None,
        )
        tree.apply(1, 6, "x")
        tree.apply(3, 7, "y")
        expected = "axxyyyy"
        for l in range(8):
            for r in range(l, 8):
                self.assertEqual(tree.prod(l, r), expected[l:r])
        self.assertEqual(tree.all_prod(), expected)

    def test_empty_and_invalid_ranges(self):
        for n in (0, 1, 5):
            tree = affine_tree([0] * n)
            tree.apply(0, n, (1, 7))
            for p in range(n + 1):
                tree.apply(p, p, (0, 99))
                self.assertEqual(tree.prod(p, p), (0, 0))
            self.assertEqual(tree.all_prod(), (7 * n, n))
            for l, r in ((-1, 0), (0, n + 1), (1, 0)):
                with self.assertRaises(IndexError):
                    tree.prod(l, r)
                with self.assertRaises(IndexError):
                    tree.apply(l, r, (1, 1))
            for p in (-1, n):
                with self.assertRaises(IndexError):
                    tree.get(p)
                with self.assertRaises(IndexError):
                    tree.set(p, (1, 1))


if __name__ == "__main__":
    unittest.main()
