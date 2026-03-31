import math

# --- 1. SETTINGS & DATA ---
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

# --- 2. THE FORMULAS ---

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
        time_budget = T_max - (n * t_r)
        if time_budget <= 0: break
        cn = min(math.floor(time_budget / tc), (n + 1) * cf_base)
        if cn > best:
            best = cn
            n_star = n
        else: break
    c0 = min(math.floor(T_max / tc), cf_base)
    return {"n_star": n_star, "c_with": best, "c_none": c0, "gain": best - c0}

def v_star(D_km, tank, a0, beta, T_max=480):
    """Critical speed where Time limit = Fuel limit"""
    cf = math.floor(tank / f_cycle(D_km, a0, beta))
    return cf * D_km * 60.0 * beta / T_max

# --- 3. FINAL REPORTS ---

# A. Optimal Speed v* Analysis (Cell 8)
print("\n" + "="*80)
print(" Optimal Speed v* per Vehicle (No Traffic)")
print("="*80)
print(f"{'Vehicle':<18} {'C_fuel':>7} {'v* (kph)':>10} Interpretation")
print("-" * 75)

for name, vd in VEHICLES.items():
    vs = v_star(D_km, vd["tank"], vd["a0"], 1.00)
    cf = math.floor(vd["tank"] / f_cycle(D_km, vd["a0"], 1.00))
    note = "fuel-limited at 30 kph" if vs < 30 else "time-limited at 30 kph"
    print(f"{name:<18} {cf:>7} {vs:>10.1f} {note}")

print("\nConclusion:")
print("1. For Aerox and Suzuki GD, v* < 30 kph, so they remain fuel-limited.")
print("2. For all others, v* > 30 kph, so 30 kph is time-limited (best available).")

# B. Refuelling Gains Summary
t_r = 12.5
print(f"\n" + "="*80)
print(f" Mid-shift Refuelling Gains (tr=12.5m, 30kph, No Traffic)")
print("="*80)
for name, vd in VEHICLES.items():
    r = c_max_refuel(D_km, 30, 1.00, vd["tank"], vd["a0"], t_r)
    if r['gain'] > 0:
        print(f"{name:<18}: Optimized n*={r['n_star']} | New C_max={r['c_with']} (+{r['gain']} cycles)")
    else:
        print(f"{name:<18}: Refuelling provides no gain (Time-bound)")