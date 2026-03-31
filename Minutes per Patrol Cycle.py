# --- 1. GLOBAL CONSTANTS ---
D_km = 9.8785  # kilometres
T_MAX = 480    # minutes (8-hour shift)
SPEEDS = [10, 20, 30]

# --- 2. DATA STRUCTURES ---
# Removed extra spaces in keys to prevent lookup errors
VEHICLES = {
    "Aerox (Chief)": {"kmL": 40, "tank": 5.5, "a0": 1/40, "role": "Chief ng Tanod"},
    "Bajaj CT110":   {"kmL": 71, "tank": 11.0, "a0": 1/71, "role": "Patrol 1"},
    "Suzuki GD":     {"kmL": 11, "tank": 9.2, "a0": 1/11, "role": "Patrol 2"},
    "Suzuki APV":    {"kmL": 11, "tank": 46.0, "a0": 1/11, "role": "Support Van"},
    "Nissan NV350":  {"kmL": 13, "tank": 65.0, "a0": 1/13, "role": "Transport"},
}

SHIFTS = {
    "No Traffic": {"p": 0.00, "beta": 1.00},
    "Morning":    {"p": 0.20, "beta": 1.20},
    "Afternoon":  {"p": 0.40, "beta": 1.40},
    "Night":      {"p": 0.05, "beta": 1.05},
}

# These must be defined here so "Cell 3" can see them
SHIFT_NAMES = list(SHIFTS.keys())

# --- 3. FUNCTIONS ---
def traffic_multiplier(p_s: float) -> float:
    return 1.0 + p_s

def t_cycle(D_km: float, v_kph: float, beta: float) -> float:
    """T_cycle = (D_km / v) * 60 * beta [minutes]"""
    return (D_km / v_kph) * 60.0 * beta

# --- 4. OUTPUT: MINUTES PER CYCLE ---
print("Minutes per Cycle (identical for all 5 vehicles)")
print(f"{'Speed':>8}", end="")
for sh in SHIFT_NAMES:
    print(f" {sh:>12}", end="")
print()
print("-" * 65)

for v in SPEEDS:
    print(f"{v:>5} kph", end="")
    for sh, data in SHIFTS.items():
        tc = t_cycle(D_km, v, data["beta"])
        print(f" {tc:>12.2f}", end="")
    print()

# Verification
ex = t_cycle(9.8785, 30, 1.40)
print(f"\nNumerical example (30 kph, Afternoon): {ex:.2f} min (paper: 27.66)")