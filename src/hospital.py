import random

class hospital:

    def __init__(self, id, x, y, insurers):
        self.id = id
        self.x = x
        self.y = y
        self.insurers = insurers

    def __repr__(self):
        return f"Hosiptal(id={self.id}, x={self.x:.1f},y={self.y:.1f})"

def dist2(h, qx, qy):
    dx = h.x - qx
    dy = h.y - qy
    return dx * dx + dy * dy

def generate_hospitals(n, coverage, seed=42):
    rng = random.Random(seed)
    hospitals = []
    for i in range(n):
        x = rng.uniform(0, 100)
        y = rng.uniform(0, 100)

        insurers = {name for name, p in coverage.items() if rng.random() < p}

        hospitals.append(hospital(i, x, y, insurers))
    return hospitals