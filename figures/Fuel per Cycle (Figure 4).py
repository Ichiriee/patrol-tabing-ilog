import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. DATA SETUP ---
D_km = 9.8785
# Single horizontal line names
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]

VEHICLES = {
    "Aerox (Chief)": {"a0": 0.0222},
    "Bajaj CT110": {"a0": 0.0333},
    "Suzuki GD (Patrol 2)": {"a0": 0.0222},
    "Suzuki APV": {"a0": 0.1000},
    "Nissan NV350": {"a0": 0.0909}
}

SHIFTS = {
    "No Traffic": {"beta": 1.00},
    "Morning": {"beta": 1.20},
    "Afternoon": {"beta": 1.40},
    "Night": {"beta": 1.05},
}

# Colors assigned per shift as per your SHIFT_COLORS variable
SHIFT_COLORS = {
    "No Traffic": "#2ecc71",
    "Morning": "#f1c40f",
    "Afternoon": "#e74c3c",
    "Night": "#34495e",
}


def f_cycle(dist, a0, beta):
    return dist * a0 * beta


# --- 2. PLOTTING ---
fig, ax = plt.subplots(figsize=(15, 8))
x = np.arange(len(VEHICLE_NAMES))
w = 0.18
colors = list(SHIFT_COLORS.values())

table_data = []
shift_names = list(SHIFTS.keys())

for i, (sh_name, sh_data) in enumerate(SHIFTS.items()):
    vals = [f_cycle(D_km, VEHICLES[n]["a0"], sh_data["beta"]) for n in VEHICLE_NAMES]
    table_data.append([f"{v:.3f}" for v in vals])

    # Plot bars
    for j, val in enumerate(vals):
        bar_x = x[j] + (i - 1.5) * w
        ax.bar(bar_x, val, w, color=colors[i], edgecolor="black", linewidth=0.5)

        # ADDED: Numerical label on top of each bar
        ax.text(bar_x, val + 0.01, f"{val:.2f}",
                ha='center', va='bottom', fontsize=8, fontweight='bold', rotation=0)

# --- 3. DATA TABLE ---
the_table = ax.table(cellText=table_data,
                     rowLabels=shift_names,
                     rowColours=colors,
                     colLabels=VEHICLE_NAMES,
                     loc='bottom',
                     cellLoc='center',
                     bbox=[0, -0.35, 1, 0.25])

the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

# Formatting
ax.set_xticks([])
ax.set_ylabel("Fuel per Cycle (Litres)", fontsize=10, fontweight="bold")
ax.set_title(r"Fuel per Cycle Analysis - $F_{\mathrm{cycle}} = D_{\mathrm{km}} \times a_0 \times \beta_s$",
             fontsize=12, fontweight="bold", pad=25)

# Legend moved to top to avoid bar obstruction
patches = [mpatches.Patch(color=c, label=s) for s, c in SHIFT_COLORS.items()]
ax.legend(handles=patches, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 0.94), frameon=True)

ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_ylim(0, 1.6)  # Headroom for top labels

plt.tight_layout(rect=[0, 0.05, 1, 0.90])
plt.savefig("fig_fcycle_final.png", dpi=150, bbox_inches="tight")
plt.show()