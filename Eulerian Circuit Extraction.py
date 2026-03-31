import networkx as nx
import numpy as np

# --- 1. DEFINE THE ROAD NETWORK DATA ---
# This list contains all 82 street segments (u, v, length in meters)
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

# Build the Graph (G)
G = nx.Graph()
for u, v, w in EDGES:
    G.add_edge(u, v, weight=w)

# --- 2. SOLVE CHINESE POSTMAN PROBLEM (CPP) ---

# Find nodes with odd degrees (requiring extra coverage)
odd_verts = sorted([v for v in G.nodes() if G.degree(v) % 2 == 1])

# Calculate distance matrix between odd nodes
n_odd = len(odd_verts)
dist_matrix = np.zeros((n_odd, n_odd))
for i, u in enumerate(odd_verts):
    lengths = nx.single_source_dijkstra_path_length(G, u, weight="weight")
    for j, v in enumerate(odd_verts):
        dist_matrix[i, j] = lengths[v]

# Run Blossom Algorithm to find matching pairs that minimize extra distance
K = nx.Graph()
for i, u in enumerate(odd_verts):
    for j, v in enumerate(odd_verts):
        if i < j:
            K.add_edge(u, v, weight=dist_matrix[i, j])
matching = nx.min_weight_matching(K)

# --- 3. BUILD AUGMENTED MULTIGRAPH (G_aug) ---

G_aug = nx.MultiGraph(G)
for u, v in matching:
    # Find shortest path between matched odd nodes and duplicate edges
    path = nx.shortest_path(G, u, v, weight="weight")
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        G_aug.add_edge(a, b, weight=G[a][b]["weight"])

# --- 4. EXTRACT EULERIAN PATROL CIRCUIT ---

circuit = list(nx.eulerian_circuit(G_aug, source=1))
circuit_nodes = [circuit[0][0]] + [v for _, v in circuit]
total_dist = sum(G[u][v]["weight"] for u, v in circuit)

# --- 5. FORMAL SUMMARY OUTPUT ---

print("-" * 60)
print(f" {'FINAL PATROL ROUTE EXTRACTION (CPP)':^58}")
print("-" * 60)
print(f" G_aug Nodes Even        : {all(G_aug.degree(v) % 2 == 0 for v in G_aug.nodes())}")
print(f" Total Edges Traversed   : {len(circuit)}")
print(f" Start/End at HQ (v1)    : {circuit_nodes[0] == 1 and circuit_nodes[-1] == 1}")
print(f" Total Patrol Distance   : {total_dist:.2f} meters")
print(f" (Verification Target    : 9,878.5 meters)")

print("\n PATROL SEQUENCE PREVIEW:")
print(f" First 15 nodes: {' -> '.join('v'+str(x) for x in circuit_nodes[:15])}")
print(f" Last 10 nodes : {' -> '.join('v'+str(x) for x in circuit_nodes[-10:])}")
print("-" * 60)