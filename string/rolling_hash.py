from secrets import randbelow


_MOD = (1 << 61) - 1
_BASE = randbelow(_MOD - 257) + 257


class RollingHash:
    def __init__(self, text, base=_BASE):
        if not 1 < base < _MOD:
            raise ValueError("base must satisfy 1 < base < 2**61 - 1")
        self.n = len(text)
        self.base = base
        self.prefix = [0] * (self.n + 1)
        self.power = [1] * (self.n + 1)
        for i, char in enumerate(text):
            self.prefix[i + 1] = (self.prefix[i] * base + ord(char) + 1) % _MOD
            self.power[i + 1] = self.power[i] * base % _MOD

    def get(self, l, r):
        if not 0 <= l <= r <= self.n:
            raise IndexError("range must satisfy 0 <= l <= r <= n")
        return (self.prefix[r] - self.prefix[l] * self.power[r - l]) % _MOD
