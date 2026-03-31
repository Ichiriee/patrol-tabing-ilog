import networkx as nx
import numpy as np

# --- 1. DEFINE THE ROAD NETWORK (CELL 10) ---
# Edges: (node_u, node_v, distance_in_meters)
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

# Build the Graph
G = nx.Graph()
for u, v, w in EDGES:
    G.add_edge(u, v, weight=w)

# --- 2. DIJKSTRA PAIRWISE DISTANCES (CELL 11) ---
# Identify nodes that need extra coverage (Odd Degree Nodes)
odd_verts = sorted([v for v in G.nodes() if G.degree(v) % 2 == 1])
n_odd = len(odd_verts)
dist_matrix = np.zeros((n_odd, n_odd))

# Calculate shortest path between every pair of odd nodes
for i, u in enumerate(odd_verts):
    lengths = nx.single_source_dijkstra_path_length(G, u, weight="weight")
    for j, v in enumerate(odd_verts):
        dist_matrix[i, j] = lengths[v]

# --- 3. MINIMUM WEIGHT PERFECT MATCHING / BLOSSOM (CELL 12) ---
# Create auxiliary graph of odd nodes only
K = nx.Graph()
for i, u in enumerate(odd_verts):
    for j, v in enumerate(odd_verts):
        if i < j:
            K.add_edge(u, v, weight=dist_matrix[i, j])

# Run Blossom Algorithm
matching = nx.min_weight_matching(K)

# Format the matching results
pairs = []
for u, v in matching:
    i = odd_verts.index(u)
    j = odd_verts.index(v)
    pairs.append((u, v, dist_matrix[i, j]))

pairs.sort(key=lambda x: x[2]) # Sort by distance
total_overhead = sum(d for _, _, d in pairs)

# --- 4. PRINT FORMAL SUMMARY ---
print("-" * 60)
print(f" {'CHINESE POSTMAN PROBLEM (CPP) SUMMARY':^58}")
print("-" * 60)
print(f" Odd-Degree Nodes Found  : {len(odd_verts)}")
print(f" Corrective Pairs Matched : {len(pairs)}")

base_length = sum(w for _, _, w in EDGES)
cpp_total = base_length + total_overhead

print(f"\n Base Network Length     : {base_length:9.2f} m")
print(f" Deadheading Overhead    : {total_overhead:9.2f} m")
print(f" Total Tour Length (D_km): {cpp_total:9.2f} m")
print(f" Overhead Ratio          : {(total_overhead/base_length)*100:.2f}%")
print("-" * 60)

# Optional: Print the specific paths
print("\n MATCHED PAIRS & PATHS:")
for idx, (u, v, d) in enumerate(pairs, 1):
    path = nx.shortest_path(G, u, v, weight="weight")
    print(f"{idx:>2}. v{u:<2} - v{v:<2} ({d:>6.1f}m) : {' -> '.join(map(str, path))}")