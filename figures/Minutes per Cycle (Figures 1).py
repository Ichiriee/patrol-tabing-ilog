import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION & DATA ---
D_km = 9.8785
SPEED = 10
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]
SHIFTS = ["No Traffic", "Morning", "Afternoon", "Night"]
BETAS = [1.00, 1.20, 1.40, 1.05]
SHIFT_COLORS = ["#2ecc71", "#f1c40f", "#e74c3c", "#34495e"]


def t_cycle(dist, speed, beta):
    return (dist / speed) * 60.0 * beta


# --- 2. PLOTTING FIGURE (10 kph) ---
fig, ax = plt.subplots(figsize=(12, 8))  # Slightly taller to accommodate table and top legend
x = np.arange(len(VEHICLE_NAMES))
w = 0.18
table_data = []

for i, (sh_name, beta) in enumerate(zip(SHIFTS, BETAS)):
    val = t_cycle(D_km, SPEED, beta)
    table_data.append([f"{val:.1f}"] * len(VEHICLE_NAMES))

    for j in range(len(VEHICLE_NAMES)):
        bar_x = x[j] + (i - 1.5) * w
        ax.bar(bar_x, val, w, color=SHIFT_COLORS[i], edgecolor="black", linewidth=0.5)
        # Data labels on top
        ax.text(bar_x, val + 0.5, f"{val:.1f}", ha='center', va='bottom', fontsize=8, fontweight='bold')

# --- 3. DATA TABLE ---
the_table = ax.table(cellText=table_data, rowLabels=SHIFTS, rowColours=SHIFT_COLORS,
                     colLabels=VEHICLE_NAMES, loc='bottom', cellLoc='center', bbox=[0, -0.35, 1, 0.25])
the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

# Formatting
ax.set_xticks([])
ax.set_ylabel("Minutes per Cycle", fontweight="bold")
ax.set_title(f"Cycle Duration Analysis at {SPEED} kph", fontsize=12, fontweight="bold", pad=35)
ax.set_ylim(0, t_cycle(D_km, SPEED, 1.4) * 1.2)  # Added extra headroom for labels
ax.grid(axis='y', linestyle='--', alpha=0.3)

# --- 4. LEGEND (REPOSITIONED TO AVOID OBSTRUCTION) ---
# Moved higher using bbox_to_anchor and set to 4 columns to be thin
patches = [mpatches.Patch(color=SHIFT_COLORS[i], label=SHIFTS[i]) for i in range(4)]
ax.legend(handles=patches, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.12),
          frameon=True, fontsize=10)

# Adjusted top rect from 0.92 to 0.88 to make room for the legend
plt.tight_layout(rect=[0, 0.05, 1, 0.88])
plt.show()