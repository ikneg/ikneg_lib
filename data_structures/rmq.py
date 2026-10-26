class rmq:
    def __init__(self, n):
        self.siz = 1
        while self.siz < n:
            self.siz *= 2
        self.dat = [0] * (self.siz * 2 + 1)

    def update(self, pos, x):
        pos += self.siz - 1
        self.dat[pos] = x
        while pos >= 2:
            pos //= 2
            self.dat[pos] = max(self.dat[pos * 2], self.dat[pos * 2 + 1])

    def query(self, l, r, a=None, b=None, u=1):
        if a is None:
            a = 1
        if b is None:
            b = self.siz + 1
        if r <= a or b <= l:
            return float("-inf")
        if l <= a and b <= r:
            return self.dat[u]
        mid = (a + b) // 2
        left = self.query(l, r, a, mid, u * 2)
        right = self.query(l, r, mid, b, u * 2 + 1)
        return max(left, right)
