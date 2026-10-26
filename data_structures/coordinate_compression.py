def coordinate_compress(values):
    values = list(values)
    originals = sorted(set(values))
    ranks = {value: i for i, value in enumerate(originals)}
    return [ranks[value] for value in values], originals
