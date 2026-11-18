from src.kdtree import build, nearest_k

def prepare_strategy_a(hospitals, network):
    trees = {}
    for insurer, ids in network.items():
        members = [h for h in hospitals if h.id in ids]
        trees[insurer] = build(members)
    return trees

def strategy_a(tress, qx, qy, insurer, k):
    return nearest_k(tress.get(insurer),qx, qy, k)

def strategy_b(root, network, n_total, qx, qy, insurer, k):
    ids = network.get(insurer, set())
    if not ids:
        return []

    want = k
    while True:
        candidates = nearest_k(root, qx, qy, want)
        good = [(d, h) for d, h in candidates if h.id in ids]

        if len(good) >= k or want >= n_total:
            return good[:k]

        want *= 2

def strategy_c(root, network, qx, qy, insurer, k):
    ids = network.get(insurer, set())
    if not ids:
        return []

    return nearest_k(root, qx, qy, k, accept= lambda h:h.id in ids)

