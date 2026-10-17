class rmq:
    def __init__(self, n):
        self.siz = 1
        while self.siz < n:
          self.siz *= 2
          
          
        self.dat = [0] * (self.siz * 2 + 1 )
        

    def update(self, pos, x):
        pos = pos + self.siz - 1
        self.dat[pos] = x
        while pos >= 2:
            pos //= 2
            self.dat[pos] = max(self.dat[pos * 2], self.dat[pos*2 + 1])

    def query(self, l, r, a, b, u):
        if r <= a or b <= l: return -100000000000
        if l <= a and b <= r: return self.dat[u]

        m = (a + b) // 2
        AnswerL = self.query(l, r, a, m, u * 2)
        AnswerR = self.query(l, r, m, b, u * 2 + 1)
        return max(AnswerL, AnswerR)
        

# T.update(pos, x)
# print(T.query(l, r, 1, T.siz + 1, 1))
    