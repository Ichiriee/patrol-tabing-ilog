import math

# --- PART 1: GLOBAL SETTINGS & DATA ---
D_km = 9.8785  # Patrol cycle distance (km)
T_MAX = 480    # 8-hour shift (minutes)
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

# --- PART 2: THE MATHEMATICAL FORMULAS ---

def traffic_multiplier(p_s):
    return 1.0 + p_s

def t_cycle(D_km, v, beta):
    """Time per cycle in minutes"""
    return (D_km / v) * 60.0 * beta

def f_cycle(D_km, a0, beta):
    """Fuel per cycle in Litres"""
    return D_km * a0 * beta

def c_max(D_km, v_kph, beta, tank, a0, T_max=480):
    """Finds max cycles based on time vs fuel constraints"""
    tc = t_cycle(D_km, v_kph, beta)
    fc = f_cycle(D_km, a0, beta)
    ct = math.floor(T_max / tc)
    cf = math.floor(tank / fc)
    cm = min(ct, cf)
    binding = "Time" if ct <= cf else "Fuel"
    return cm, ct, cf, binding

def c_max_refuel(D_km, v_kph, beta, tank, a0, t_r, T_max=480):
    """Finds optimal refuelling stops (n*) to maximize cycles"""
    tc = t_cycle(D_km, v_kph, beta)
    fc = f_cycle(D_km, a0, beta)
    cf_base = math.floor(tank / fc)
    best = min(math.floor(T_max / tc), cf_base)
    n_star = 0
    for n in range(1, 20):
        time_budget = T_max - (n * t_r)
        if time_budget <= 0: break
        cn = min(math.floor(time_budget / tc), (n + 1) * cf_base)
        if cn > best:
            best = cn
            n_star = n
        else: break
    c0 = min(math.floor(T_max / tc), cf_base)
    return {"n_star": n_star, "c_with": best, "c_none": c0, "gain": best - c0}

def c_empty(D_km, tank, a0, beta):
    """Cycles until tank is empty (speed-independent)"""
    return math.floor(tank / f_cycle(D_km, a0, beta))

# --- PART 3: OUTPUT & REPORTS ---

# A. Fleet Summary
print(f"{'Vehicle':<18} {'km/L':>5} {'Tank':>6} {'a0 (L/km)':>11} {'Role'}")
print("-" * 65)
for name, v in VEHICLES.items():
    print(f"{name:<18} {v['kmL']:>5} {v['tank']:>5}L {v['a0']:>11.5f} {v['role']}")

# B. Fuel per Cycle Table
print("\n--- Fuel per Cycle (Litres) ---")
for name, vd in VEHICLES.items():
    print(f"{name:<18}", end="")
    for sh, sdata in SHIFTS.items():
        fc = f_cycle(D_km, vd["a0"], sdata["beta"])
        print(f" {fc:>10.3f}L", end="")
    print()

# C. C_max Tables (10, 20, 30 kph)
for speed in SPEEDS:
    print(f"\n{'='*80}\n C_max at {speed} kph\n{'='*80}")
    print(f"{'Vehicle':<18} {'No Traffic':>12} {'Morning':>10} {'Afternoon':>12} {'Night':>8} Binding")
    print("-" * 80)
    for name, vd in VEHICLES.items():
        row = [c_max(D_km, speed, s["beta"], vd["tank"], vd["a0"])[0] for s in SHIFTS.values()]
        b = c_max(D_km, speed, SHIFTS["No Traffic"]["beta"], vd["tank"], vd["a0"])[3]
        print(f"{name:<18} {row[0]:>12} {row[1]:>10} {row[2]:>12} {row[3]:>8} {b}")

# D. Refuelling Optimization (Cell 6)
t_r = 12.5
speed = 30
print(f"\n{'='*80}\nMid-shift Refuelling (tr=12.5m, 30kph)\n" + "-"*80)
print(f"{'Vehicle':<18} {'C(0)':>6} {'n*':>5} {'C(n*)':>7} {'Gain':>6} Time used")
for name, vd in VEHICLES.items():
    r = c_max_refuel(D_km, speed, SHIFTS["No Traffic"]["beta"], vd["tank"], vd["a0"], t_r)
    tc_val = t_cycle(D_km, speed, SHIFTS["No Traffic"]["beta"])
    time_used = r["c_with"] * tc_val + r["n_star"] * t_r
    gain_str = f"+{r['gain']}" if r["gain"] > 0 else " "
    print(f"{name:<18} {r['c_none']:>6} {r['n_star']:>5} {r['c_with']:>7} {gain_str:>6} {time_used:>10.1f}m")

# E. Cycles Until Empty (Cell 7)
print(f"\n{'='*80}\n Cycles Until Full Tank Empty (Speed-independent)\n" + "="*80)
print(f"{'Vehicle':<18} {'Tank':>6} {'No Traffic':>12} {'Morning':>10} {'Afternoon':>12} {'Night':>8}")
print("-" * 80)
for name, vd in VEHICLES.items():
    row = [c_empty(D_km, vd["tank"], vd["a0"], s["beta"]) for s in SHIFTS.values()]
    print(f"{name:<18} {vd['tank']:>5.1f}L {row[0]:>12} {row[1]:>10} {row[2]:>12} {row[3]:>8}")

# F. Worked Examples & Checks
print("\n--- Final Checks ---")
ex_nv350 = c_empty(9.8785, 65.0, 1/13, 1.00)
print(f"NV350 No Traffic: {ex_nv350} cycles (Target: 85)")
ex_gd = c_max(9.8785, 30, 1.40, 9.2, 1/11)[0]
print(f"Suzuki GD Afternoon 30kph: {ex_gd} cycles")