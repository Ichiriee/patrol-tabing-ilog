import math
import networkx as nx

# --- 1. GLOBAL PARAMETERS & DATA STRUCTURES ---
# Constants for the patrol environment
D_KM = 9.8785  # Total cycle distance in kilometers
T_MAX = 480  # Total shift duration in minutes (8 hours)
SPEEDS = [10, 20, 30]  # Patrol speeds in kph

# Fleet specifications: Fuel efficiency (km/L), tank capacity (L), and role
VEHICLES = {
    "Aerox (Chief)": {"kmL": 40, "tank": 5.5, "a0": 1 / 40, "role": "Chief ng Tanod"},
    "Bajaj CT110": {"kmL": 71, "tank": 11.0, "a0": 1 / 71, "role": "Patrol 1"},
    "Suzuki GD": {"kmL": 11, "tank": 9.2, "a0": 1 / 11, "role": "Patrol 2"},
    "Suzuki APV": {"kmL": 11, "tank": 46.0, "a0": 1 / 11, "role": "Support Van"},
    "Nissan NV350": {"kmL": 13, "tank": 65.0, "a0": 1 / 13, "role": "Transport"},
}

# Shift-specific traffic congestion parameters (beta)
SHIFTS = {
    "No Traffic": {"p": 0.00, "beta": 1.00},
    "Morning": {"p": 0.20, "beta": 1.20},
    "Afternoon": {"p": 0.40, "beta": 1.40},
    "Night": {"p": 0.05, "beta": 1.05},
}


# --- 2. OPERATIONAL CALCULATION FUNCTIONS ---

def t_cycle(dist, speed, beta):
    """Calculates time duration per cycle in minutes."""
    return (dist / speed) * 60.0 * beta


def f_cycle(dist, fuel_rate, beta):
    """Calculates fuel consumption per cycle in Litres."""
    return dist * fuel_rate * beta


def c_max(dist, speed, beta, tank, fuel_rate, shift_limit=480):
    """
    Determines the maximum possible cycles per shift.
    Constraint: min(Time-limited cycles, Fuel-limited cycles)
    """
    tc = t_cycle(dist, speed, beta)
    fc = f_cycle(dist, fuel_rate, beta)

    ct = math.floor(shift_limit / tc)
    cf = math.floor(tank / fc)

    cm = min(ct, cf)
    binding_constraint = "Time" if ct <= cf else "Fuel"
    return cm, ct, cf, binding_constraint


# --- 3. ROAD NETWORK GRAPH CONSTRUCTION (CELL 10) ---

# Edge list representing the Tabing-Ilog road network (u, v, weight in meters)
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

# Initialize and populate the undirected weighted graph
G = nx.Graph()
for u, v, w in EDGES:
    G.add_edge(u, v, weight=w)

# --- 4. NETWORK ANALYSIS & OUTPUT ---

total_road_length = sum(w for _, _, w in EDGES)
avg_edge_length = total_road_length / len(EDGES)
odd_nodes = [v for v in G.nodes() if G.degree(v) % 2 == 1]
is_eulerian = nx.is_eulerian(G)
is_connected = nx.is_connected(G)

print("\n" + "-" * 55)
print(" STRUCTURAL PROPERTIES: TABING-ILOG PATROL GRAPH")
print("-" * 55)
print(f" Total Vertices (Nodes)      : {G.number_of_nodes()}")
print(f" Total Edges (Segments)      : {G.number_of_edges()}")
print(f" Total Network Length        : {total_road_length:.2f} meters")
print(f" Mean Segment Length         : {avg_edge_length:.2f} meters")
print(f" Odd-Degree Node Count       : {len(odd_nodes)}")
print(f" Eulerian Circuit Possible   : {is_eulerian}")
print(f" Graph Connectivity Status   : {is_connected}")
print("-" * 55)