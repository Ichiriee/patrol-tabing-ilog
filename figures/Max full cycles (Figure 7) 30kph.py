import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION & DATA ---
D_km = 9.8785
SPEED = 30
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]

VEHICLES = {
    "Aerox (Chief)":      {"tank": 4.2,  "a0": 0.0222},
    "Bajaj CT110":        {"tank": 8.0,  "a0": 0.0333},
    "Suzuki GD (Patrol 2)":{"tank": 8.5,  "a0": 0.0350},
    "Suzuki APV":          {"tank": 46.0, "a0": 0.1000},
    "Nissan NV350":       {"tank": 50.0, "a0": 0.0909}
}

SHIFTS = ["No Traffic", "Morning", "Afternoon", "Night"]
BETAS = [1.00, 1.20, 1.40, 1.05]
SHIFT_COLORS = ["#2ecc71", "#f1c40f", "#e74c3c", "#34495e"]

def c_max(dist, speed, beta, tank, a0):
    t_c = (dist / speed) * 60.0 * beta
    f_c = dist * a0 * beta
    limit_time = int(480 / t_c)
    limit_fuel = int(tank / f_c)
    return min(limit_time, limit_fuel)

# --- 2. PLOTTING ---
fig, ax = plt.subplots(figsize=(12, 8))
x = np.arange(len(VEHICLE_NAMES))
w = 0.18
table_data = []

for i, (sh_name, beta) in enumerate(zip(SHIFTS, BETAS)):
    vals = [c_max(D_km, SPEED, beta, VEHICLES[n]["tank"], VEHICLES[n]["a0"]) for n in VEHICLE_NAMES]
    table_data.append([str(v) for v in vals])

    for j, val in enumerate(vals):
        bar_x = x[j] + (i - 1.5) * w
        ax.bar(bar_x, val, w, color=SHIFT_COLORS[i], edgecolor="black", linewidth=0.5)
        ax.text(bar_x, val + 0.4, str(val), ha='center', va='bottom', fontsize=8, fontweight='bold')

the_table = ax.table(cellText=table_data, rowLabels=SHIFTS, rowColours=SHIFT_COLORS,
                     colLabels=VEHICLE_NAMES, loc='bottom', cellLoc='center', bbox=[0, -0.35, 1, 0.25])
the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

ax.set_xticks([])
ax.set_ylabel("Max Full Cycles (count)", fontweight="bold")
ax.set_title(f"Max Cycles per 8-Hour Shift at {SPEED} kph", fontsize=12, fontweight="bold", pad=35)
ax.set_ylim(0, 35)
ax.grid(axis='y', linestyle='--', alpha=0.3)

patches = [mpatches.Patch(color=SHIFT_COLORS[i], label=SHIFTS[i]) for i in range(4)]
ax.legend(handles=patches, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.12), frameon=True)

plt.tight_layout(rect=[0, 0.05, 1, 0.88])
plt.show()