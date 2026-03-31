import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION & DATA ---
# Single horizontal line names for the table
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]
SHIFTS = ["No Traffic", "Morning", "Afternoon", "Night"]
SHIFT_COLORS = ["#2ecc71", "#f1c40f", "#e74c3c", "#34495e"]

# Data from your refuelling analysis
# Rows represent shifts to match the table format
with_refuel_data = np.array([
    [23, 24, 23, 24, 24],  # No Traffic
    [19, 20, 19, 20, 20],  # Morning
    [16, 17, 16, 17, 17],  # Afternoon
    [22, 23, 21, 23, 23]  # Night
])

# --- 2. PLOTTING ---
fig, ax = plt.subplots(figsize=(12, 8))
x = np.arange(len(VEHICLE_NAMES))
w = 0.18

table_data = []

for i in range(len(SHIFTS)):
    vals = with_refuel_data[i]
    table_data.append([str(v) for v in vals])

    for j, val in enumerate(vals):
        bar_x = x[j] + (i - 1.5) * w
        # Bars colored by shift
        ax.bar(bar_x, val, w, color=SHIFT_COLORS[i], edgecolor="black", linewidth=0.5)

        # Add the number on top of each bar
        ax.text(bar_x, val + 0.3, str(val), ha='center', va='bottom',
                fontsize=9, fontweight='bold')

# --- 3. DATA TABLE ---
the_table = ax.table(cellText=table_data,
                     rowLabels=SHIFTS,
                     rowColours=SHIFT_COLORS,
                     colLabels=VEHICLE_NAMES,
                     loc='bottom',
                     cellLoc='center',
                     bbox=[0, -0.35, 1, 0.25])

the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

# Formatting
ax.set_xticks([])  # Hide default x-ticks for the table
ax.set_ylabel("Max Full Cycles per 8-Hour Shift", fontweight="bold")
ax.set_title("Max Cycles per Shift: With Optimal Refuelling (30 kph)",
             fontsize=12, fontweight="bold", pad=40)
ax.set_ylim(0, 30)
ax.grid(axis='y', linestyle='--', alpha=0.3)

# --- 4. LEGEND (REPOSITIONED TO TOP) ---
patches = [mpatches.Patch(color=SHIFT_COLORS[i], label=SHIFTS[i]) for i in range(4)]
ax.legend(handles=patches, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.13),
          frameon=True, fontsize=10)

plt.tight_layout(rect=[0, 0.05, 1, 0.88])
plt.show()