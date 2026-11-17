import random
from src.hospital import generate_hospitals
from src.brute_force import brute_force
from src.kdtree import build, nearest_k

COVERAGE = {"Star": 1.0}

def test_matches_brute_force():
    hospitals = generate_hospitals(2000, COVERAGE, seed = 1)
    root = build(hospitals)
    rng = random.Random(99)

    for _ in range(1000):
        qx, qy = rng.uniform(0, 1000), rng.uniform(0,100)
        expected = brute_force(hospitals, qx, qy, "Star", 5)
        got = nearest_k(root, qx, qy, 5)

        assert [d for d, h in got] == [d for d, h in expected]

def test_k_larger_than_n():
    hospitals = generate_hospitals(3, COVERAGE, seed=1)
    root = build(hospitals)
    assert len(nearest_k(root, 50 ,50, 10)) == 3

def test_empty_tree():
    assert nearest_k(build([]), 0, 0, 5) == []