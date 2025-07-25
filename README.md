<h1 align="center" style="color:#4CAF50;">
  🛡️ Fence Tension & Tamper Detection System
</h1>

<p align="center">
  <em>Real-time magnetic field visualizer with 3D tension modeling and tamper detection alerts</em><br>
  <strong>By Lovejoy Mhishi</strong>
</p>

---

## 🌟 What It Does

This Python-based system connects to a microcontroller (like an Arduino or ESP32) and:

- 📶 **Reads real-time magnetic field data** via serial (Bx, By, Bz)
- 📊 **Plots field values and rate of change** in 2D over time
- 🧵 **Visualizes fence tension as a 3D curve**
- 🚨 **Detects tampering** using magnetic thresholds and rate-of-change triggers
- 🔔 **Triggers audible alarms** when suspicious activity is detected
- 📈 Displays **count of breaches** and **elapsed time** since the last breach

---

## 🧠 Core Concepts

The program assumes:
- A magnetic sensor is mounted on or near the fence
- External disturbances (tugging, vibrations) cause sudden changes in field strength or direction
- Thresholds (`Z_THR`, `X_THR`) and derivatives (`dBx`, `dBy`, `dBz`) signal possible tampering

---

## 🎥 Real-Time Visuals

### 1️⃣ **3D Tension Plot**
- A Bézier curve represents the tensioned wire
- The magnetic field vector influences the curve shape
- Additional strands simulate the full wire array

### 2️⃣ **2D Magnetic Field Graph**
- Shows `Bx`, `By`, `Bz` vs. time  
- Overlaid with `Z_THR` and `X_THR` for context

### 3️⃣ **2D Derivative Graph**
- Visualizes the **rate of change** (`dBx/dt`, `dBy/dt`, `dBz/dt`)
- Threshold line (ΔB_THR = 2 mT/sample) indicates alarm zone

---

## 🚨 Tamper Alerts

If any of the following is true:

- `bz < Z_THR` or `bz > X_THR`
- `dBx`, `dBy`, or `dBz` exceeds **2 mT/sample**

Then:
- A **red alert message** is shown in the 3D plot
- A **beep alert** is triggered using `winsound.Beep()`

---

## 📦 Serial Data Format

The incoming serial line must follow this format:

