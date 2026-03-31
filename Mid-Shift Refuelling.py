import math

# --- 1. SETTINGS & DATA ---
D_km = 9.8785  # distance per cycle in km
T_MAX = 480    # 8-hour shift in minutes
SPEEDS = [10, 20, 30] # kph

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
SHIFT_NAMES = list(SHIFTS.keys())

# --- 2. THE FORMULAS ---

def traffic_multiplier(p_s):
    return 1.0 + p_s

def t_cycle(D_km, v, beta):
    return (D_km / v) * 60.0 * beta

def f_cycle(D_km, a0, beta):
    return D_km * a0 * beta

def c_max(D_km, v_kph, beta, tank, a0, T_max=480):
    tc = t_cycle(D_km, v_kph, beta)
    fc = f_cycle(D_km, a0, beta)
    ct = math.floor(T_max / tc)
    cf = math.floor(tank / fc)
    cm = min(ct, cf)
    binding = "Time" if ct <= cf else "Fuel"
    return cm, ct, cf, binding

def c_max_refuel(D_km, v_kph, beta, tank, a0, t_r, T_max=480):
    tc = t_cycle(D_km, v_kph, beta)
    fc = f_cycle(D_km, a0, beta)
    cf_base = math.floor(tank / fc)
    best = min(math.floor(T_max / tc), cf_base)
    n_star = 0
    for n in range(1, 20):
        time_budget = T_max - n * t_r
        if time_budget <= 0: break
        cn = min(math.floor(time_budget / tc), (n + 1) * cf_base)
        if cn > best:
            best = cn
            n_star = n
        else: break
    c0 = min(math.floor(T_max / tc), cf_base)
    return {"n_star": n_star, "c_with": best, "c_none": c0, "gain": best - c0}

# --- 3. EXECUTION & TABLES ---

# A. Fleet Summary
print(f"{'Vehicle':<18} {'km/L':>5} {'Tank':>6} {'a0 (L/km)':>11} {'Role'}")
print("-" * 65)
for name, v in VEHICLES.items():
    print(f"{name:<18} {v['kmL']:>5} {v['tank']:>5}L {v['a0']:>11.5f} {v['role']}")

# B. Fuel per Cycle
print("\n--- Fuel per Cycle (Litres) ---")
for name, vd in VEHICLES.items():
    print(f"{name:<18}", end="")
    for sh, sdata in SHIFTS.items():
        fc = f_cycle(D_km, vd["a0"], sdata["beta"])
        print(f" {fc:>10.3f}L", end="")
    print()

# C. C_max Tables for all Speeds
for speed in SPEEDS:
    print(f"\n{'='*80}")
    print(f" C_max at {speed} kph (Max cycles before shift end or empty tank)")
    print(f"{'='*80}")
    print(f"{'Vehicle':<18} {'No Traffic':>12} {'Morning':>10} {'Afternoon':>12} {'Night':>8} Binding")
    print("-" * 80)
    for name, vd in VEHICLES.items():
        row = []
        bindings = []
        for sh, sdata in SHIFTS.items():
            cm, ct, cf, b = c_max(D_km, speed, sdata["beta"], vd["tank"], vd["a0"])
            row.append(cm)
            bindings.append(b)
        print(f"{name:<18} {row[0]:>12} {row[1]:>10} {row[2]:>12} {row[3]:>8} {bindings[0]}")

# D. Mid-shift Refuelling (Cell 6)
t_r = 12.5
speed = 30
beta = SHIFTS["No Traffic"]["beta"]
print(f"\n{'='*80}\nMid-shift refuelling | {speed} kph | No Traffic | t_r = {t_r} min\n" + "-"*80)
print(f"{'Vehicle':<18} {'C(0)':>6} {'n*':>5} {'C(n*)':>7} {'Gain':>6} Time used (min)")

for name, vd in VEHICLES.items():
    r = c_max_refuel(D_km, speed, beta, vd["tank"], vd["a0"], t_r)
    tc_val = t_cycle(D_km, speed, beta)
    time_used = r["c_with"] * tc_val + r["n_star"] * t_r
    gain_str = f"+{r['gain']}" if r["gain"] > 0 else " "
    print(f"{name:<18} {r['c_none']:>6} {r['n_star']:>5} {r['c_with']:>7} {gain_str:>6} {time_used:>12.1f}")

# E. Worked Example: Suzuki GD
print("\n--- Worked example: Suzuki GD ---")
vd = VEHICLES["Suzuki GD"]
tc = t_cycle(D_km, speed, beta)
fc = f_cycle(D_km, vd["a0"], beta)
cf0 = math.floor(vd["tank"] / fc)
for n in range(4):
    ct_n = math.floor((T_MAX - n * t_r) / tc)
    cf_n = (n + 1) * cf0
    cn = min(ct_n, cf_n)
    print(f"n={n}: min(floor({(T_MAX - n*t_r):.1f}/{tc:.2f})={ct_n}, {cf_n}) = {cn}")