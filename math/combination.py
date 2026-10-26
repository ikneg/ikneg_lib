class Combination:
    def __init__(self, n, mod=998244353):
        if n < 0 or mod <= 1:
            raise ValueError("n must be nonnegative and mod must exceed 1")
        self.n = n
        self.mod = mod
        self.fact = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fact[i] = self.fact[i - 1] * i % mod
        self.inv_fact = [1] * (n + 1)
        self.inv_fact[n] = pow(self.fact[n], -1, mod)
        for i in range(n, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % mod

    def comb(self, n, r):
        if not 0 <= n <= self.n:
            raise ValueError("n must be within the precomputed range")
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod


def binomial_coefficients(n):
    if n < 0:
        raise ValueError("n must be nonnegative")
    result = [1]
    for r in range(n):
        result.append(result[-1] * (n - r) // (r + 1))
    return result
