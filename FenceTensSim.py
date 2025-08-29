import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import winsound
import csv
import time

# --- Serial setup ---
ser = serial.Serial('COM5', 115200, timeout=5)
time.sleep(2)
print("Connected to:", ser.name)

# --- CSV setup (once, before loop) ---
csvfile = open("SBT_data_logger.csv", mode="w", newline='')
fieldnames = ["Timestamp", "FenceBreachCount", "Bx", "By", "Bz","X_THR_min","Z_THR_max", "Temperature", "SecondCount"]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
prev_hour = time.strftime("%H")

# --- 3D plot setup ---
plt.ion()
fig1 = plt.figure(figsize=(8, 6))
ax3d = fig1.add_subplot(111, projection='3d')

p0 = np.array([0, 0, 0])
p2 = np.array([8, 0, 0])
stretch_scale = 0.5
offset = 0.2  # vertical offset for extra strands

# --- 2D plot setup (Field values) ---
fig2, ax2d = plt.subplots(figsize=(8, 4))
ax2d.set_facecolor("#cccccc")
x_vals = deque(maxlen=100)
bx_vals = deque(maxlen=100)
by_vals = deque(maxlen=100)
bz_vals = deque(maxlen=100)
z_thr = deque(maxlen=100)
z_thr_min = deque(maxlen=100)
x_thr = deque(maxlen=100)
x_thr_max = deque(maxlen=100)

line_bx, = ax2d.plot([], [], label='Bx')
line_by, = ax2d.plot([], [], label='By')
line_bz, = ax2d.plot([], [], label='Bz')
line_z_thr, = ax2d.plot([], [], 'g-.', label='Z_THR', linewidth=1.5)
line_z_thr_min, = ax2d.plot([], [], 'g-.', label='', linewidth=1.5)
line_x_thr, = ax2d.plot([], [], color='#1f77b4', linestyle='-.', label='X_THR', linewidth=1.5)
line_x_thr_max, = ax2d.plot([], [], color='#1f77b4', linestyle='-.', label='', linewidth=1.5)

ax2d.set_xlabel('Sample')
ax2d.set_ylabel('Magnetic Field (mT)')
ax2d.set_title('Real-Time Magnetic Field Readings')
ax2d.legend()
ax2d.grid(True)

# --- 2D plot setup (Rate of Change) ---
fig3, ax_deriv = plt.subplots(figsize=(8, 4))
ax_deriv.set_facecolor("#cacaca")
bx_deriv = deque(maxlen=100)
by_deriv = deque(maxlen=100)
bz_deriv = deque(maxlen=100)

line_dbx, = ax_deriv.plot([], [], label='dBx/dt')
line_dby, = ax_deriv.plot([], [], label='dBy/dt')
line_dbz, = ax_deriv.plot([], [], label='dBz/dt')
line_DB, = ax_deriv.plot([], [], 'r-.', label='ΔB_THR', linewidth=1.5)

ax_deriv.set_xlabel('Sample')
ax_deriv.set_ylabel('ΔB (mT/sample)')
ax_deriv.set_title('The Change in Magnetic Fields')
ax_deriv.legend()
ax_deriv.grid(True)


# --- 2D plot setup (Fig 4: B-field + Temperature) ---
fig4, ax4_left = plt.subplots(figsize=(10, 5))
ax4_right = ax4_left.twinx()  # create right y-axis

time_vals = deque(maxlen=60)  # last 60 minutes
bx_vals_plot = deque(maxlen=60)
by_vals_plot = deque(maxlen=60)
bz_vals_plot = deque(maxlen=60)
temp_vals_plot = deque(maxlen=60)

line_bx4, = ax4_left.plot([], [], label='Bx')
line_by4, = ax4_left.plot([], [], label='By')
line_bz4, = ax4_left.plot([], [], label='Bz')
line_temp4, = ax4_right.plot([], [], label='Temperature', color='r', linestyle='--')

ax4_left.set_xlabel('Time')
ax4_left.set_ylabel('Magnetic Field (mT)')
ax4_right.set_ylabel('Temperature (°C)')
ax4_left.set_title('Real-Time B-fields and Temperature')
ax4_left.legend(loc='upper left')
ax4_right.legend(loc='upper right')
ax4_left.grid(True)


# --- Main loop ---
i = 0
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        try:
            parts = line.split()
            bx = float(parts[0].split('=')[1]) / 1
            by = float(parts[1].split('=')[1]) / 100
            bz = float(parts[2].split('=')[1]) / 1
            Z_THR = float(parts[3].split('=')[1]) /10 
            Z_THR_min = float(parts[3].split('=')[1]) /10 - 6

            X_THR = float(parts[4].split('=')[1]) /10
            X_THR_max = float(parts[4].split('=')[1]) /10 + 6

            dbx = float(parts[5].split('=')[1]) / 10
            dby = float(parts[6].split('=')[1]) / 10
            dbz = float(parts[7].split('=')[1]) / 1
            FenceBreachCount= float(parts[8].split('=')[1]) + 1
            TimeElasped = float(parts[9].split('=')[1])
            Time = float(parts[10].split('=')[1])
            ADC = float(parts[11].split('=')[1])/10
            Temperature = float(parts[12].split('=')[1])
            DeltaTemp = float(parts[13].split('=')[1])

             # Prepare row
            row = {
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "FenceBreachCount": FenceBreachCount,
                "Bx":bx,
                "By":by,
                "Bz":bz,
                "Z_THR_min":X_THR,
                "Z_THR_max":Z_THR,
                "Temperature": Temperature,
                "SecondCount": Time
           }
            
            curr_hour = time.strftime("%H")
            if curr_hour != prev_hour:
                 # Write row to CSV
                 writer.writerow(row)
                 csvfile.flush()
                 print(row)

                 time_vals.append(curr_hour)
                 bx_vals_plot.append(bx)
                 by_vals_plot.append(by)
                 bz_vals_plot.append(bz)
                 temp_vals_plot.append(Temperature)


                 line_bx4.set_data(time_vals, bx_vals_plot)
                 line_by4.set_data(time_vals, by_vals_plot)
                 line_bz4.set_data(time_vals, bz_vals_plot)
                 line_temp4.set_data(time_vals, temp_vals_plot)

                  # Set x-limits as last 60 entries
                 ax4_left.set_xlim(time_vals[0], time_vals[-1] if len(time_vals) > 1 else time_vals[0])

                 
                 all_b_vals = list(bx_vals_plot) + list(by_vals_plot) + list(bz_vals_plot)
                 ax4_left.set_ylim(min(all_b_vals) - 1, max(all_b_vals) + 1)

                 # Set y-limits for right axis
                 ax4_right.set_ylim(min(temp_vals_plot) - 1, max(temp_vals_plot) + 1)

                 fig4.canvas.draw()
                 fig4.canvas.flush_events()
                 prev_hour =  curr_hour
           
            #print(f"Magnetic Fields: Bx={bx:.3f}, By={by:.3f}, Bz={bz:.3f}, X_THR={X_THR}, Z_THR={Z_THR}")
        except (IndexError, ValueError):
            continue

        # --- 3D plot ---
        B = np.array([bx, 0, bz - Z_THR + 2.1])
        B_norm = np.linalg.norm(B)
        B_unit = B / B_norm if B_norm > 0 else np.array([0, 0, 0])

        center = (p0 + p2) / 2
        p1 = center + stretch_scale * B_unit

        t_vals = np.linspace(0, 1, 30)
        curve = [(1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2 for t in t_vals]
        curve = np.array(curve)
        xs, ys, zs = curve[:, 0], curve[:, 1], curve[:, 2]

        ax3d.cla()
        ax3d.set_xlim([-1, 10])
        ax3d.set_ylim([-1, 1])
        ax3d.set_zlim([-1, 1])
        ax3d.set_title("Fence Tension")
        ax3d.set_axis_off()
        ax3d.view_init(elev=9, azim=-22)

        # Ground plane
        Xg = np.array([[-1, 10], [-1, 10]])
        Yg = np.array([[-1, -1], [1, 1]])
        Zg = np.array([[-1, -1], [-1, -1]])
        ax3d.plot_surface(Xg, Yg, Zg, color='black', alpha=0.4)

            # Example variables
        text_str = (
            f"FenceBreachCount: {FenceBreachCount}\n"
            f"FenceBreachPeriod: {TimeElasped}s\n"
            f"--------.......--------........\n"
        )

        text_strng =(
            f"TimeCount: {Time}s\n" 
            f"ADC_VUNREG: {ADC}V\n"
            f"Temperature: {Temperature}°C\n"
            f"ΔTemp: {DeltaTemp}°C"
             
        )

        ax3d.text2D(
            0.95, 0.95, text_str,
            transform=ax3d.transAxes,
            ha='left',
            va='top',
            fontsize=10,
            color='black',
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor='#d3d3d3',
                edgecolor='black',
                alpha=0.7
            )
        )

        ax3d.text2D(
            0.1, 0.95, text_strng,
            transform=ax3d.transAxes,
            ha='right',
            va='top',
            fontsize=10,
            color='black',
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="#9b5959",
                edgecolor='black',
                alpha=0.7
            )
        )

        if (bz < Z_THR_min or bz > Z_THR or bx < X_THR or bz > X_THR_max or dbx > 2 or dby > 2 or dbz > 2):
            winsound.Beep(1000, 200)
            ax3d.text(0, 0, 1.4, "Tampering Detected!!!", color='red', fontsize=11, weight='bold')

        # Poles
        ax3d.plot([p0[0], p0[0]], [p0[1], p0[1]], [-1, p0[2]+0.5], color='black', linewidth=10)
        ax3d.plot([p2[0], p2[0]], [p2[1], p2[1]], [-1, p2[2]+0.5], color='black', linewidth=10)

        # Original curved wire
        ax3d.plot(xs, ys, zs, color='red', linewidth=2)

        # Extra straight strands
        top_p0 = p0 + np.array([0, 0, offset])
        top_p2 = p2 + np.array([0, 0, offset])
        ax3d.plot([top_p0[0], top_p2[0]], [top_p0[1], top_p2[1]], [top_p0[2], top_p2[2]], color='gray', linewidth=2)

        bottom_p0 = p0 + np.array([0, 0, -offset])
        bottom_p2 = p2 + np.array([0, 0, -offset])
        ax3d.plot([bottom_p0[0], bottom_p2[0]], [bottom_p0[1], bottom_p2[1]], [bottom_p0[2], bottom_p2[2]], color='gray', linewidth=2)

        fig1.canvas.draw()
        fig1.canvas.flush_events()

        # --- Real-time 2D Plot (Field values) ---
        x_vals.append(i)
        bx_vals.append(bx)
        by_vals.append(by)
        bz_vals.append(bz)
        z_thr.append(Z_THR)
        z_thr_min.append( Z_THR_min)
        x_thr.append(X_THR)
        x_thr_max.append(X_THR_max)

        line_bx.set_data(x_vals, bx_vals)
        line_by.set_data(x_vals, by_vals)
        line_bz.set_data(x_vals, bz_vals)
        line_z_thr.set_data(x_vals, z_thr)
        line_z_thr_min.set_data(x_vals, z_thr_min)
        line_x_thr.set_data(x_vals, x_thr)
        line_x_thr_max.set_data(x_vals, x_thr_max)

        ax2d.set_xlim(max(0, i - 100), i + 1)
        all_b_vals = list(bx_vals) + list(by_vals) + list(bz_vals) + list(z_thr) + list(x_thr) + list(z_thr_min) + list(x_thr_max) 
        ymin, ymax = min(all_b_vals), max(all_b_vals)
        ax2d.set_ylim(ymin - 1, ymax + 1)

        fig2.canvas.draw()
        fig2.canvas.flush_events()

        # --- Rate of Change Plot ---
        bx_deriv.append(dbx)
        by_deriv.append(dby)
        bz_deriv.append(dbz)

        line_dbx.set_data(x_vals, bx_deriv)
        line_dby.set_data(x_vals, by_deriv)
        line_dbz.set_data(x_vals, bz_deriv)
        line_DB.set_data(x_vals,[2]*len(x_vals))

        ax_deriv.set_xlim(max(0, i - 100), i + 1)
        all_derivs = list(bx_deriv) + list(by_deriv) + list(bz_deriv)
        ymin_d, ymax_d = -2, max(all_derivs)
        ax_deriv.set_ylim(ymin_d - 0.1, ymax_d + 2)

        fig3.canvas.draw()
        fig3.canvas.flush_events()

        plt.pause(0.05)
        i += 1

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    ser.close()
    plt.ioff()
    plt.show()
