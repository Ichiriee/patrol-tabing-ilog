import math
import networkx as nx
import numpy as np

# --- 1. DATA AND GRAPH SETUP ---
# All 82 edges from the Tabing-Ilog road network
EDGES = [
    (1, 2, 158.64), (1, 29, 54.05), (2, 3, 42.4), (2, 9, 78.25),
    (3, 4, 78.25), (3, 8, 75.89), (3, 29, 250.0), (5, 8, 47.0),
    (6, 10, 88.06), (7, 11, 89.03), (8, 9, 43.1), (9, 10, 40.0),
    (10, 11, 33.1), (11, 12, 92.0), (12, 13, 38.0), (12, 23, 239.31),
    (13, 14, 35.0), (13, 20, 195.0), (14, 15, 33.44), (14, 21, 180.0),
    (15, 16, 18.46), (15, 17, 130.0), (16, 18, 110.0), (17, 18, 29.0),
    (17, 22, 33.79), (18, 19, 31.87), (18, 25, 130.0), (19, 26, 140.0),
    (20, 21, 60.0), (21, 22, 36.14), (21, 24, 85.0), (22, 24, 100.0),
    (23, 24, 130.0), (24, 25, 49.0), (24, 27, 42.0), (25, 26, 30.5),
    (26, 28, 34.32), (27, 28, 84.5), (29, 30, 150.0), (30, 31, 160.0),
    (30, 37, 63.6), (31, 32, 50.3), (32, 33, 16.82), (32, 34, 14.88),
    (33, 35, 26.0), (35, 36, 40.2), (37, 38, 60.0), (37, 43, 31.07),
    (38, 39, 152.95), (39, 40, 173.7), (39, 41, 183.8), (41, 42, 70.35),
    (41, 44, 180.0), (43, 44, 118.4), (44, 45, 53.0), (45, 46, 19.36),
    (45, 48, 69.12), (46, 47, 56.89), (47, 48, 60.39), (48, 49, 36.85),
    (49, 50, 150.0), (49, 51, 213.0), (51, 52, 170.0), (51, 53, 69.78),
    (53, 54, 142.31), (53, 55, 112.41), (55, 56, 79.2), (55, 64, 93.0),
    (56, 57, 39.86), (56, 58, 140.0), (58, 59, 73.48), (59, 60, 12.51),
    (59, 63, 13.57), (60, 61, 67.35), (61, 62, 43.41), (62, 63, 76.57),
    (64, 65, 110.0), (64, 69, 82.24), (65, 66, 65.59), (66, 67, 54.27),
    (66, 68, 49.68), (68, 69, 69.12),
]

G = nx.Graph()
for u, v, w in EDGES:
    G.add_edge(u, v, weight=w)

base_length = sum(w for _, _, w in EDGES)
odd_verts = sorted([v for v in G.nodes() if G.degree(v) % 2 == 1])

# Incident counts per edge (from barangay records, N_max = 10)
INCIDENTS = {
    (24, 25): 10, (21, 22): 8, (20, 21): 7, (14, 21): 6, (13, 14): 5,
    (22, 24): 4, (17, 22): 3, (15, 17): 2, (12, 23): 2, (18, 25): 1,
}
N_MAX = 10


# --- 2. HOTSPOT FUNCTIONS ---

def h_score(u, v):
    """Calculates normalized hotspot risk score h(u,v)."""
    key = (min(u, v), max(u, v))
    return INCIDENTS.get(key, 0) / N_MAX


def hotspot_dist_matrix(alpha):
    """Builds the distance matrix for odd nodes using distance + alpha*risk."""
    n = len(odd_verts)
    mat = np.zeros((n, n))
    for i, u in enumerate(odd_verts):
        # Weight function: physical distance + weighted risk score
        lengths = nx.single_source_dijkstra_path_length(
            G, u, weight=lambda u, v, d: d['weight'] + (alpha * h_score(u, v))
        )
        for j, v in enumerate(odd_verts):
            mat[i, j] = lengths[v]
    return mat


# --- 3. SENSITIVITY ANALYSIS EXECUTION ---

print("\n" + "=" * 80)
print(f"{'Alpha':>6} {'Extra (m)':>12} {'Total Route (m)':>18} {'Overhead %':>12} {'Pairs Redirected':>18}")
print("-" * 80)

baseline_matching = None

for alpha in [0, 50, 100, 200, 500]:
    mat = hotspot_dist_matrix(alpha)
    Kh = nx.Graph()
    for i, u in enumerate(odd_verts):
        for j, v in enumerate(odd_verts):
            if i < j:
                Kh.add_edge(u, v, weight=mat[i, j])

    # Solve matching (Blossom Algorithm)
    m = nx.min_weight_matching(Kh)

    # Calculate physical distance overhead (excluding alpha weight)
    overhead = 0
    current_set = set()
    for u, v in m:
        d_phys = nx.shortest_path_length(G, u, v, weight="weight")
        overhead += d_phys
        current_set.add(tuple(sorted((u, v))))

    total = base_length + overhead
    overhead_pct = (overhead / base_length) * 100

    if alpha == 0:
        baseline_matching = current_set
        redirected = 0
    else:
        # Count how many node pairs changed compared to alpha=0
        redirected = len(current_set - baseline_matching)

    print(f"{alpha:>6} {overhead:>12.1f} {total:>18.1f} {overhead_pct:>11.2f}% {redirected:>18}")

print("-" * 80)