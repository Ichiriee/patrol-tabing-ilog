import math

# --- 1. RE-DEFINE THE DATA ---
D_km = 9.8785
T_MAX = 480
SPEEDS = [10, 20, 30]

VEHICLES = {
    "Aerox (Chief)": {"kmL": 40, "tank": 5.5, "a0": 1 / 40, "role": "Chief ng Tanod"},
    "Bajaj CT110": {"kmL": 71, "tank": 11.0, "a0": 1 / 71, "role": "Patrol 1"},
    "Suzuki GD": {"kmL": 11, "tank": 9.2, "a0": 1 / 11, "role": "Patrol 2"},
    "Suzuki APV": {"kmL": 11, "tank": 46.0, "a0": 1 / 11, "role": "Support Van"},
    "Nissan NV350": {"kmL": 13, "tank": 65.0, "a0": 1 / 13, "role": "Transport"},
}

SHIFTS = {
    "No Traffic": {"p": 0.00, "beta": 1.00},
    "Morning": {"p": 0.20, "beta": 1.20},
    "Afternoon": {"p": 0.40, "beta": 1.40},
    "Night": {"p": 0.05, "beta": 1.05},
}


# --- 2. RE-DEFINE THE BASIC FUNCTIONS ---
def t_cycle(D_km, v, beta):
    return (D_km / v) * 60.0 * beta


def f_cycle(D_km, a0, beta):
    return D_km * a0 * beta


# --- 3. THE NEW C_MAX FUNCTIONS ---
def c_max(D_km, v_kph, beta, tank, a0, T_max=480):
    tc = t_cycle(D_km, v_kph, beta)
    fc = f_cycle(D_km, a0, beta)
    ct = math.floor(T_max / tc)
    cf = math.floor(tank / fc)
    cm = min(ct, cf)
    binding = "Time" if ct <= cf else "Fuel"
    return cm, ct, cf, binding


# --- 4. PRINT THE TABLES ---
for speed in SPEEDS:
    print(f"\n{'=' * 75}")
    print(f" C_max at {speed} kph")
    print(f"{'=' * 75}")
    print(f"{'Vehicle':<18} {'No Traffic':>12} {'Morning':>10} {'Afternoon':>12} {'Night':>8} Binding")
    print("-" * 75)

    for name, vd in VEHICLES.items():
        row = []
        bindings = []
        for sh, sdata in SHIFTS.items():
            cm, ct, cf, b = c_max(D_km, speed, sdata["beta"], vd["tank"], vd["a0"])
            row.append(cm)
            bindings.append(b)

        binding_ref = bindings[0]
        print(f"{name:<18} {row[0]:>12} {row[1]:>10} {row[2]:>12} {row[3]:>8} {binding_ref}")