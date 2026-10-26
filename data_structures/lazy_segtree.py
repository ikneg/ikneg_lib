class LazySegmentTree:
    def __init__(self, values, op, e, mapping, composition, id_):
        values = list(values)
        self.n = len(values)
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id_
        self.log = (max(1, self.n) - 1).bit_length()
        self.size = 1 << self.log
        self.data = [e] * (2 * self.size)
        self.lazy = [id_] * self.size
        self.data[self.size:self.size + self.n] = values
        for k in range(self.size - 1, 0, -1):
            self._update(k)

    def _update(self, k):
        self.data[k] = self.op(self.data[2 * k], self.data[2 * k + 1])

    def _all_apply(self, k, f):
        self.data[k] = self.mapping(f, self.data[k])
        if k < self.size:
            self.lazy[k] = self.composition(f, self.lazy[k])

    def _push(self, k):
        self._all_apply(2 * k, self.lazy[k])
        self._all_apply(2 * k + 1, self.lazy[k])
        self.lazy[k] = self.id

    def _check_index(self, p):
        if not 0 <= p < self.n:
            raise IndexError("index must satisfy 0 <= p < n")

    def _check_range(self, l, r):
        if not 0 <= l <= r <= self.n:
            raise IndexError("range must satisfy 0 <= l <= r <= n")

    def set(self, p, x):
        self._check_index(p)
        p += self.size
        for i in range(self.log, 0, -1):
            self._push(p >> i)
        self.data[p] = x
        for i in range(1, self.log + 1):
            self._update(p >> i)

    def get(self, p):
        self._check_index(p)
        p += self.size
        for i in range(self.log, 0, -1):
            self._push(p >> i)
        return self.data[p]

    def prod(self, l, r):
        self._check_range(l, r)
        if l == r:
            return self.e
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if (l >> i) << i != l:
                self._push(l >> i)
            if (r >> i) << i != r:
                self._push((r - 1) >> i)
        left = right = self.e
        while l < r:
            if l & 1:
                left = self.op(left, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                right = self.op(self.data[r], right)
            l >>= 1
            r >>= 1
        return self.op(left, right)

    def all_prod(self):
        return self.data[1]

    def apply(self, l, r, f):
        self._check_range(l, r)
        if l == r:
            return
        l += self.size
        r += self.size
        for i in range(self.log, 0, -1):
            if (l >> i) << i != l:
                self._push(l >> i)
            if (r >> i) << i != r:
                self._push((r - 1) >> i)
        start, end = l, r
        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1
        for i in range(1, self.log + 1):
            if (start >> i) << i != start:
                self._update(start >> i)
            if (end >> i) << i != end:
                self._update((end - 1) >> i)
