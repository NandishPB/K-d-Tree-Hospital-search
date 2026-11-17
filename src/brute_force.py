from src.hospital import dist2

def brute_force(hospitals, qx,qy, insurer, k):
    matches = []
    for h in hospitals:
        if insurer in h.insurers:
            matches.append((dist2(h, qx, qy), h))

    matches.sort(key=lambda pair:(pair[0], pair[1].id))

    return matches[:k]
