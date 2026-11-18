from src.hospital import generate_hospitals
from src.network import build_network_index

def test_index_matches_hospitals():
    hospitals = generate_hospitals(1000, {'Star':0.3, 'HDFC':0.05}, seed=3)
    index = build_network_index(hospitals)

    for h in hospitals:
        for name in ("Star", "HDFC"):
            assert (h.id in index.get(name, set())) == (name in h.insurers)
            