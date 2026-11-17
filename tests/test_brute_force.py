from src.hospital import hospital
from src.brute_force import brute_force

def make_small():
    return [
        hospital(0, 0, 0, {"Star"}),
        hospital(1, 3, 4, {"Star", "HDFC"}),
        hospital(2, 10, 10, {"HDFC"}),
        hospital(3, 1, 1, {"Star"}),
        hospital(4, 50, 50, {"Star"}),
    ]

def test_star_k3():
    result = brute_force(make_small(), 0,0, "Star", 3)
    assert [h.id for d, h in result] == [0,3,1]
    assert [d for d, h in result] == [0, 2, 25]

def test_fewer_than_k():
    result = brute_force(make_small(), 0, 0, "HDFC", 5)
    assert [h.id for d, h in result] == [1,2]

def test_unknown_insurer():
    assert brute_force(make_small(), 0,0, "Nobody", 3) == []