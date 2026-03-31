import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION & DATA ---
D_km = 9.8785
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]

VEHICLES = {
    "Aerox (Chief)": {"tank": 4.2, "a0": 0.0222},
    "Bajaj CT110": {"tank": 8.0, "a0": 0.0333},
    "Suzuki GD (Patrol 2)": {"tank": 8.5, "a0": 0.0350},
    "Suzuki APV": {"tank": 46.0, "a0": 0.1000},
    "Nissan NV350": {"tank": 50.0, "a0": 0.0909}
}

SHIFTS = ["No Traffic", "Morning", "Afternoon", "Night"]
BETAS = [1.00, 1.20, 1.40, 1.05]

# Colors mapped to SHIFTS instead of vehicles
SHIFT_COLORS = ["#2ecc71", "#f1c40f", "#e74c3c", "#34495e"]

def c_empty(dist, tank, a0, beta):
    return int(tank / (dist * a0 * beta))

# --- 2. PLOTTING ---
fig, ax = plt.subplots(figsize=(15, 8))
x = np.arange(len(VEHICLE_NAMES))
w = 0.18

table_data = []

# Loop through shifts to determine bar color
for i, (sh_name, beta) in enumerate(zip(SHIFTS, BETAS)):
    vals = [c_empty(D_km, VEHICLES[n]["tank"], VEHICLES[n]["a0"], beta)
            for n in VEHICLE_NAMES]

    table_data.append([str(v) for v in vals])

    # Plotting: color is now determined by the shift index (i)
    for j, val in enumerate(vals):
        bar = ax.bar(x[j] + (i - 1.5) * w, val, w,
                     color=SHIFT_COLORS[i], edgecolor="black", linewidth=0.5, alpha=0.9)

        # Add the number on top of each bar
        ax.text(x[j] + (i - 1.5) * w, val + 0.5, str(val),
                ha='center', va='bottom', fontsize=8, fontweight='bold')

# --- 3. DATA TABLE ---
the_table = ax.table(cellText=table_data,
                     rowLabels=SHIFTS,
                     rowColours=SHIFT_COLORS, # Match row headers to bar colors
                     colLabels=VEHICLE_NAMES,
                     loc='bottom',
                     cellLoc='center',
                     bbox=[0, -0.35, 1, 0.25])

the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

# Formatting
ax.set_xticks([])
ax.set_ylabel("Cycles Until Tank Empty (count)", fontweight="bold")
ax.set_title("Cycles Until Full Tank Empty: All Vehicles & Shifts\n" +
             r"$C_{\mathrm{empty}} = \lfloor F_{\mathrm{tank}} / (D_{\mathrm{km}} \times a_0 \times \beta_s) \rfloor$",
             fontsize=12, fontweight="bold", pad=25)
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_ylim(0, 65)

# --- 4. LEGEND & TITLES ---
# Legend now represents the Shift categories
s_patches = [mpatches.Patch(color=SHIFT_COLORS[i], label=SHIFTS[i]) for i in range(4)]

fig.legend(handles=s_patches, loc="upper center", ncol=4, fontsize=10,
           bbox_to_anchor=(0.5, 0.94), frameon=True)

plt.tight_layout(rect=[0, 0.05, 1, 0.90])
plt.savefig("fig_cempty_shift_colors.png", dpi=150, bbox_inches="tight")
plt.show()