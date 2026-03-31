# --- PART 1: DEFINITIONS ---
D_km = 9.8785  # kilometres
T_MAX = 480  # minutes

# Note: Removed extra spaces in keys like " Morning " -> "Morning"
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


# --- PART 2: FUNCTIONS ---
def traffic_multiplier(p_s: float) -> float:
    return 1.0 + p_s


# --- PART 3: EXECUTION ---
print(f"{'Shift':<14} {'p_s':>6} {'_s':>6} Interpretation")
print("-" * 62)

for name, data in SHIFTS.items():
    beta = traffic_multiplier(data["p"])

    # Simple interpretation map
    interp_map = {
        "No Traffic": "Baseline no overhead",
        "Morning": "All times and fuel 1.20",
        "Afternoon": "Worst case all metrics 1.40",
        "Night": "Near-baseline, lightest overhead",
    }

    interp = interp_map.get(name, "Unknown Shift")
    print(f"{name:<14} {data['p'] * 100:>5.0f}% {beta:>5.2f} {interp}")