import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- 1. CONFIGURATION & DATA ---
# Names on 1 horizontal line
VEHICLE_NAMES = ["Aerox (Chief)", "Bajaj CT110", "Suzuki GD (Patrol 2)", "Suzuki APV", "Nissan NV350"]
SHIFTS = ["No Traffic", "Morning", "Afternoon", "Night"]
SHIFT_COLORS = ["#2ecc71", "#f1c40f", "#e74c3c", "#34495e"]

# Data for 30 kph
without_refuel = np.array([
    [22, 18, 15, 21],  # Aerox
    [24, 20, 17, 23],  # Bajaj
    [10, 8, 7, 9],  # Suzuki GD
    [24, 20, 17, 23],  # Suzuki APV
    [24, 20, 17, 23]  # Nissan
])

with_refuel = np.array([
    [23, 19, 16, 22],  # Aerox
    [24, 20, 17, 23],  # Bajaj
    [23, 19, 16, 21],  # Suzuki GD
    [24, 20, 17, 23],  # Suzuki APV
    [24, 20, 17, 23]  # Nissan
])


def plot_refuel_analysis(data, title_suffix):
    fig, ax = plt.subplots(figsize=(15, 8))
    x = np.arange(len(VEHICLE_NAMES))
    w = 0.18
    table_data = []

    # Transpose data to iterate by shift
    for i in range(len(SHIFTS)):
        vals = data[:, i]
        table_data.append([str(v) for v in vals])

        for j, val in enumerate(vals):
            bar_x = x[j] + (i - 1.5) * w
            ax.bar(bar_x, val, w, color=SHIFT_COLORS[i], edgecolor="black", linewidth=0.5)
            # Numbers on top
            ax.text(bar_x, val + 0.3, str(val), ha='center', va='bottom',
                    fontsize=9, fontweight='bold')

    # --- DATA TABLE ---
    the_table = ax.table(cellText=table_data, rowLabels=SHIFTS, rowColours=SHIFT_COLORS,
                         colLabels=VEHICLE_NAMES, loc='bottom', cellLoc='center', bbox=[0, -0.35, 1, 0.25])
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(9)

    # Formatting
    ax.set_xticks([])
    ax.set_ylabel("Max Full Cycles per 8-Hour Shift", fontweight="bold")
    ax.set_title(f"Max Cycles per Shift {title_suffix} (30 kph)\n" +
                 r"$C_{max} = \min(\lfloor (T_{max} - nt_r)/T_c \rfloor, (n+1)\lfloor F_{tank}/F_c \rfloor)$",
                 fontsize=12, fontweight="bold", pad=40)
    ax.set_ylim(0, 30)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # --- LEGEND (Positioned to avoid obstruction) ---
    patches = [mpatches.Patch(color=SHIFT_COLORS[i], label=SHIFTS[i]) for i in range(4)]
    ax.legend(handles=patches, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.13),
              frameon=True, fontsize=10)

    plt.tight_layout(rect=[0, 0.05, 1, 0.88])
    plt.show()


# Generate the two separate figures
plot_refuel_analysis(without_refuel, "Without Refuelling")
plot_refuel_analysis(with_refuel, "With Optimal Refuelling")