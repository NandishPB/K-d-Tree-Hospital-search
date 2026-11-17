import matplotlib.pyplot as plt
from src.hospital import generate_hospitals

COVERAGE = {"Star": 0.5, "HDFC": 0.1, "Niva":0.01}

hospitals = generate_hospitals(1000, COVERAGE, seed = 42)

print("First 10 Hospitals:")
for h in hospitals[:20]:
    print(f" {h} insurers = {sorted(h.insurers)}")

print("\nNetwork sizes (expected = coverage x 1000):")
for name, p in COVERAGE.items():
    count = sum(1 for h in hospitals if name in h.insurers)
    print(f" {name}:{count} hospitals (expected about {p* 1000:.0f})")

star = [h for h in hospitals if "Star" in h.insurers]
niva = [h for h in hospitals if "Niva" in h.insurers]

plt.figure(figsize = (7, 7))
plt.scatter([h.x for h in hospitals], [h.y for h in hospitals], s=6,
            color = "lightgrey", label="All Hospitals")
plt.scatter([h.x for h in star], [h.y for h in star], s=6, 
            color="tab:blue", label="Accepts Star")
plt.scatter([h.x for h in niva], [h.y for h in niva], s=40,
            color="tab:red", label="Accepts Niva (rare)")
plt.xlabel("x (km)")
plt.ylabel("y (km)")
plt.title("Synthetic hospital map (1000 hospitals)")
plt.legend()
plt.savefig("hospital_map.png", dpi=150)
print("\nSaved hospital_map.png")