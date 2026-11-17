from src.hospital import generate_hospitals

COVERAGE = {"Star" : 0.5, "HDFC": 0.1, "Niva": 0.01}

def test_count():
    assert len(generate_hospitals(500, COVERAGE)) == 500

def test_same_seed_same_data():
    a = generate_hospitals(200, COVERAGE, seed = 7)
    b = generate_hospitals(200, COVERAGE, seed = 7)
    assert [(h.x, h.y, h.insurers) for h in a] == [(h.x, h.y, h.insurers) for h in b]

def test_coverage_is_roughly_right():
    hs = generate_hospitals(10000, COVERAGE)
    count = sum(1 for h in hs if "HDFC" in  h.insurers)
    assert 850 < count < 1150