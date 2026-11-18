import random 
from src.hospital import generate_hospitals
from src.brute_force import brute_force
from src.kdtree import build
from src.network import build_network_index
from src.strategies import prepare_strategy_a, strategy_a, strategy_b, strategy_c

def test_all_strategies_matc_brute_force():
    for p in(0.005,0.05, 0.5, 0.95):
        hospitals = generate_hospitals(2000, {"X":p}, seed = 11)
        network = build_network_index(hospitals)
        root = build(hospitals)
        trees = prepare_strategy_a(hospitals, network)
        rng = random.Random(5)

        for _ in range(300):
            qx, qy = rng.uniform(0, 100), rng.uniform(0, 100)
            expected = [d for d, h in brute_force(hospitals, qx, qy, "X", 5)]
            assert [d for d, h in strategy_a(trees, qx, qy, "X", 5)] == expected
            assert [d for d, h in strategy_b(root, network, len(hospitals), qx, qy, "X", 5)] == expected
            assert [d for d, h in strategy_c(root, network, qx, qy, "X", 5)] == expected

def test_unknown_insurer_all_empty():
    hospitals = generate_hospitals(100, {"X":0.5}, seed = 1)
    network = build_network_index(hospitals)
    root = build(hospitals)
    trees = prepare_strategy_a(hospitals, network)
    assert strategy_a(trees, 1,1, "Nobody", 5) == []
    assert strategy_b(root, network, 100, 1,1 ,"Nobody", 5) == []
    assert strategy_c(root, network, 1,1, "Nobody", 5) == []

    