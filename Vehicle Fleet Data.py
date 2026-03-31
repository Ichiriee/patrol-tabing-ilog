D_m = 9878.5 # metres
D_km = 9.8785 # kilometres
T_MAX = 480 # minutes (8-hour shift)

# Vehicle data: name -> { economy km/L, tank L, a0 L/km, role }
VEHICLES = {
    "Aerox (Chief)": {
        "kmL": 40, "tank": 5.5,
        "a0": 1/40, "role": "Chief ng Tanod"
    },
    "Bajaj CT110": {
        "kmL": 71, "tank": 11.0,
        "a0": 1/71, "role": "Patrol 1"
    },
    "Suzuki GD": {
        "kmL": 11, "tank": 9.2,
        "a0": 1/11, "role": "Patrol 2"
        # The stray '2' was removed from here
    },
    "Suzuki APV": {
        "kmL": 11, "tank": 46.0,
        "a0": 1/11, "role": "Support Van"
    },
    "Nissan NV350": {
        "kmL": 13, "tank": 65.0,
        "a0": 1/13, "role": "Transport"
    },
}

VEHICLE_NAMES = list(VEHICLES.keys())

# Traffic shifts: name -> (penalty %, beta multiplier)
SHIFTS = {
    "No Traffic": {"p": 0.00, "beta": 1.00},
    "Morning": {"p": 0.20, "beta": 1.20},
    "Afternoon": {"p": 0.40, "beta": 1.40},
    "Night": {"p": 0.05, "beta": 1.05},
}

SHIFT_NAMES = list(SHIFTS.keys())
BETAS = [s["beta"] for s in SHIFTS.values()]

# Patrol speeds to evaluate (kph)
SPEEDS = [10, 20, 30]

# Print fleet summary (Fixed the quotes and spacing here)
print(f"{'Vehicle':<18} {'km/L':>5} {'Tank':>6} {'a0 (L/km)':>11} {'Role'}")
print("-" * 60)

for name, v in VEHICLES.items():
    # Note: Use standard quotes for dictionary keys inside f-strings
    print(f"{name:<18} {v['kmL']:>5} {v['tank']:>5}L {v['a0']:>11.5f} {v['role']}")