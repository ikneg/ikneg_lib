def mod_inverse(a, mod):
    if mod <= 1:
        raise ValueError("mod must exceed 1")
    return pow(a, -1, mod)
