import csv
import random
import time

import matplotlib.pyplot as plt

from src.hospital import generate_hospitals
from src.brute_force import brute_force
from src.kdtree import build
from src.network import build_network_index
from src.strategies import prepare_strategy_a, strategy_a, strategy_b, strategy_c

SIZES = [1000, 10000, 100000]
COVERAGES = [0.01, 0.10, 0.50, 0.90]
NUM_QUERIES = 200
K = 5
INSURER = "X"

def avg_ms(fn, queries):
    start = time.perf_counter()
    for qx, qy in queries:
        fn(qx, qy)
    elapsed = time.perf_counter() - start
    return elapsed / len(queries) * 1000

def run_one(n, coverage):
    hospitals = generate_hospitals(n, {INSURER: coverage}, seed = 42)
    rng = random.Random(123)
    queries = [(rng.uniform(0,100), rng.uniform(0, 100)) for _ in range(NUM_QUERIES)]

    t = time.perf_counter(); network = build_network_index(hospitals)
    network_build_s = time.perf_counter() - t

    t = time.perf_counter(); root = build(hospitals)
    tree_build_s = time.perf_counter() - t

    t = time.perf_counter(); trees = prepare_strategy_a(hospitals, network)
    a_prepare_s = time.perf_counter() - t

    for qx, qy in queries[:30]:
        expected = [d for d, h in brute_force(hospitals, qx, qy, INSURER, K)]
        assert [d for d, h in strategy_a(trees, qx,qy, INSURER, K)] == expected
        assert [d for d, h in strategy_b(root, network, n, qx,qy, INSURER, K)] == expected
        assert [d for d, h in strategy_c(root, network, qx, qy, INSURER, K)] == expected


    return {
        "n" : n,
        "coverage" : coverage,
        "brute_ms": avg_ms(lambda x, y: brute_force(hospitals, x, y, INSURER, K), queries),
        "A_ms": avg_ms(lambda x, y: strategy_a(trees, x, y, INSURER, K), queries),
        "B_ms": avg_ms(lambda x, y: strategy_b(root, network, n, x, y, INSURER, K), queries),
        "C_ms": avg_ms(lambda x, y: strategy_c(root, network, x, y, INSURER, K), queries),
        "tree_build_s": tree_build_s,
        "A_prepare_s": a_prepare_s,
        "network_build_s": network_build_s,
    }

def main():
    rows = []
    for n in SIZES:
        for c in COVERAGES:
            print(f"running n={n}, coverage={c}...")
            row = run_one(n,c)
            rows.append(row)
            print(" ", {k: round(v, 4) if isinstance(v, float) else v for k, v in row.items()})

    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames= rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    methods = [("brute_ms", "Brute force"), ("A_ms", "A: filter-first"),
               ("B_ms", "B: search-first"), ("C_ms", "C: inline filter")]

    plt.figure()
    subset = [r for r in rows if r["coverage"] == 0.10]
    for key, label in methods:
        plt.plot([r["n"] for r in subset], [r[key] for r in subset], marker="o", label=label)
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Number of hospitals"); plt.ylabel("Avg query time (ms)")
    plt.title("Query time vs dataset size (10% network coverage)")
    plt.legend(); plt.grid(True,which="both", alpha=0.3)
    plt.savefig("graph_size.png", dpi=150)

    plt.figure()
    biggest = [r for r in rows if r["n"] == max(SIZES)]
    for key, label in methods:
        plt.plot([r["coverage"] * 100 for r in biggest], [r[key] for r in biggest],
                 marker="o", label=label)
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Insurer network coverage (% of  hospitals)"); plt.ylabel("Avg query time (ms)")
    plt.title(f"Query time vs coverage ({max(SIZES):,} hospitals)")
    plt.legend(); plt.grid(True, which="both", alpha = 0.3)
    plt.savefig("graph_coverage.png", dpi = 150)

    print("Done: results.csv, graph_size.png, graph_coverage.png")

if __name__ == "__main__":
    main()