<h1 align="center" style="color:#4CAF50;">
  🛡️ Smart Fence Monitoring System
</h1>

<p align="center">
  <em>Real-time fence tension monitoring and tamper detection system</em><br>
</p>

---

## 🌟 What It Does

This Python-based system connects to a microcontroller (like an Arduino or ESP32) and:

- 📶 **Reads real-time data** via serial (x, y, z)
- 📊 **Plots field values and rate of change** in 2D over time
- 🧵 **Visualizes fence tension as a 3D curve**
- 🚨 **Detects tampering** using defined fence thresholds and rate-of-change triggers
- 🔔 **Triggers audible alarms** when suspicious activity is detected
- 📈 Displays **count of breaches** 

---

## 🧠 Core Concepts

The program assumes:
- External disturbances (tugging, vibrations) cause sudden changes on thr fence
- Fence thresholds (`Fence0_THR`, `Fence1_THR`) and derivatives (`dx`, `dy`, `dz`) signal possible tampering

---

## 🎥 Real-Time Visuals

### 1️⃣ **3D Tension Plot**
- A Bézier curve represents the tensioned wire
- The magnetic field vector influences the curve shape
- Additional strands simulate the full wire array

### 2️⃣ **2D  Graph**
- Shows `x`, `y`, `z` vs. time  
- Overlaid with `Z_THR` and `X_THR` for context

### 3️⃣ **2D Derivative Graph**
- Visualizes the **rate of change** (`dx/dt`, `dy/dt`, `dz/dt`)
- Threshold line (ΔB_THR = 2 mT/sample) indicates alarm zone

---

## 🚨 Tamper Alerts

If any of the following is true:

- When THR are exceded
- `dx`, `dy`, or `dz` exceeds *A Defined Value*

Then:
- A **red alert message** is shown in the 3D plot
- A **beep alert** is triggered using `winsound.Beep()`

---

## 📦 Serial Data Format

The incoming serial line must follow this format:

Xx=xxxx Yy=yyyy Zz=zzzz X_THR=xxxx Z_THR=zzzz dx=xx dy=yyyy dz=zzzz FenceBreach=x Time=x.xx


> Units are expected in **microtesla**, scaled by `÷1000` in the script.

---

## 📂 Project Files
- FenceTensSim.py

---

## 👨‍💻 Built With

- **Python** (3.x)
- **Matplotlib** – 2D and 3D plotting
- **PySerial** – Serial communication
- **NumPy** – Vector math
- **winsound** – PC speaker alerts (Windows only)

---


> “Fences aren't just physical — they're smart, too.”

---


