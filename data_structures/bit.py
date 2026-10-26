class BIT:
    def __init__(self, n=0):
        self.length(n)

    def length(self, n):
        self.n = n
        self.bit = [0] * (self.n + 1)

    def add(self, i, x):
        while i <= self.n:
            self.bit[i] += x
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i

        return s
