n = 3

for bit in range(1 << n):
    selected = []

    for i in range(n):
        if bit & (1 << i):
            selected.append(i)
    print(bit)
    print(selected)