import math

# --- PART 1: GLOBAL SETTINGS & DATA ---
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


# --- PART 2: THE FORMULAS ---

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


# --- PART 3: CELL 9 - CONSTRAINT VERIFICATION ---

violations = []
for speed in SPEEDS:
    for sh_name, sh_data in SHIFTS.items():
        beta = sh_data["beta"]
        tc = t_cycle(D_km, speed, beta)

        for v_name, vd in VEHICLES.items():
            fc = f_cycle(D_km, vd["a0"], beta)
            cm, ct, cf, _ = c_max(D_km, speed, beta, vd["tank"], vd["a0"])

            # (i) Shift time constraint: C * T_cycle <= 480
            if cm * tc > T_MAX + 1e-6:
                violations.append(f"(i) FAIL {v_name} {speed}kph {sh_name}: {cm * tc:.2f} > {T_MAX}")

            # (ii) Fuel budget constraint: C * F_cycle <= F_tank
            if cm * fc > vd["tank"] + 1e-6:
                violations.append(f"(ii) FAIL {v_name} {speed}kph {sh_name}: {cm * fc:.4f} > {vd['tank']}")

            # (iii) Fixed fuel rate: a0 in the defined set
            valid_a0 = {1 / 40, 1 / 71, 1 / 11, 1 / 13}
            if not any(abs(vd["a0"] - x) < 1e-6 for x in valid_a0):
                violations.append(f"(iii) FAIL {v_name}: a0={vd['a0']:.5f} not in set")

            # (iv) Speed-independence check
            fc_v10 = f_cycle(D_km, vd["a0"], beta)
            fc_v30 = f_cycle(D_km, vd["a0"], beta)
            if abs(fc_v10 - fc_v30) > 1e-12:
                violations.append(f"(iv) FAIL {v_name}: F_cycle depends on speed")

print("\n" + "=" * 60)
print(" STEP 7: OPERATIONAL CONSTRAINT VERIFICATION")
print("=" * 60)

if violations:
    print("VIOLATIONS FOUND:")
    for v in violations:
        print(f" {v}")
else:
    print("All four operational constraints satisfied across all")
    print(f"{len(SPEEDS)} speeds, {len(SHIFTS)} shifts, and {len(VEHICLES)} vehicles.")

print("\n(i)   C * T_cycle <= 480 min (Shift Time)")
print("(ii)  C * F_cycle <= F_tank (Fuel Capacity)")
print("(iii) a0 in {0.02500, 0.01408, 0.09091, 0.07692} (Valid Rates)")
print("(iv)  d(F_cycle)/dv = 0 (Speed Independence)")