def build_network_index(hospitals):
    index = {}
    for h in hospitals:
        for name in h.insurers:
            index.setdefault(name, set()).add(h.id)
    return index