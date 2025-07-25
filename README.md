<h1 align="center" style="color:#4CAF50;">
  🌐 Fence Tension Simulator 🔧
</h1>

<p align="center">
  <em>A physics-based simulator for modeling wire tension in fencing systems</em><br>
  <strong>Built by Lovejoy Mhishi</strong>
</p>

---

## 🎯 What Is This?

The **Fence Tension Simulator** is a tool for modeling and visualizing the behavior of wire fences under mechanical tension and environmental effects.

Whether you're:
- 🔩 Designing fences in the field  
- 📈 Analyzing mechanical loads  
- 🧪 Comparing different materials  

This tool helps you understand how tension, temperature, and material type affect wire performance.

---

## ✨ Key Features

✅ Realistic tension simulation using elastic deformation models  
✅ Material selection: steel, aluminum, high-tensile wire, etc.  
✅ Temperature compensation and stress/strain visualizations  
✅ Beautiful, clear plots showing force, tension, and elongation  
✅ Optional batch configuration support using YAML  
✅ Exportable results (`.csv`, `.png`, `.svg`)

---

## 🧠 How It Works

The simulator uses physics-based equations:

- **Hooke’s Law** for force and elongation:  
  _F = k × ΔL_  
- **Thermal expansion** due to temperature changes  
- **Stress and strain** calculations across wire length  

Each simulation gives you plots and summary data that help in planning or analysis.

---

## ⚙️ Example Simulation

```bash
python simulate.py \
  --length 100 \
  --diameter 4 \
  --material steel \
  --force 600 \
  --temperature 25
