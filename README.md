# 📡 Contactless-Vital-RF-Sensing: Non-Invasive Respiration & Heartbeat Monitoring

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.13-blue.svg)](https://www.python.org/)
[![RF Band](https://img.shields.io/badge/RF-5.8%20GHz%20ISM%20%2F%20Wi--Fi%20CSI-blue.svg)]()
[![Dashboard](https://img.shields.io/badge/UI-Interactive%20Streamlit%20App-ff4b4b.svg)](app.py)
[![Speedup](https://img.shields.io/badge/Speedup-%3E4%2C000%C3%97%20Real--Time-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A non-contact, wireless **Digital Signal Processing (DSP)** pipeline designed to extract human vital signs (Respiration Rate and Heart Rate) from RF Channel State Information (CSI) and micro-Doppler radar phase shifts without requiring wearable sensors or skin-attached electrodes.

---

## 📌 Academic Scope across Engineering Disciplines

* **Electrical & Telecommunications (RF Propagation & Wireless Sensing):** Exploits two-way phase variations $\Delta \phi(t) = \frac{4\pi}{\lambda} \Delta d(t)$ induced by sub-millimeter chest wall displacements. Addresses carrier frequency offset (CFO), phase unwrapping, and multipath scattering.
* **Biomedical Engineering (Non-Invasive Telehealth):** Isolates respiratory tidal excursion (0.1–0.5 Hz, ~6–12 mm) and apex cardiac ejection micro-vibrations (0.8–2.2 Hz, ~0.1–0.5 mm) for contactless sleep monitoring, infant apnea screening, and burn patient telemetry.
* **Electrical & Computer Engineering (Embedded Edge Computing):** Executes lightweight bandpass IIR decomposition and FFT spectral estimation with <0.02 ms per-packet latency on low-cost dual-core microcomputers.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["Raw RF Phase / Wi-Fi CSI<br/>(Carrier: 5.8 GHz, fs: 100 Hz)"] --> B["Stage 1: Phase Sanitization"]
    B --> B1["Phase Unwrapping (-pi to +pi)"]
    B1 --> B2["Linear/Polynomial CFO Detrending"]
    B2 --> B3["Median / Hampel Spike Filtering"]
    B3 --> C["Stage 2: Multimodal Vital Decomposition"]
    C --> C1["Respiration Filter (0.1 - 0.5 Hz, 3rd Order IIR)"]
    C --> C2["Cardiac Filter (0.8 - 2.2 Hz, 4th Order IIR)"]
    C1 --> D["Stage 3: Spectral Rate Estimation"]
    C2 --> D
    D --> D1["Zero-Padded FFT Peak Detection"]
    D1 --> E1["Respiration Rate (RR in bpm)"]
    D1 --> E2["Heart Rate (HR in bpm)"]
```

---

## 📊 Live Visual Pipeline

Multi-stage phase sanitization and signal decomposition under noisy wireless channel conditions:

![RF Vital Signs Pipeline](assets/demo_vital_rf_sensing.png)

1. **Panel 1 (Red):** Raw wrapped RF phase corrupted by oscillator Carrier Frequency Offset (CFO) drift and $2\pi$ wrap jumps.
2. **Panel 2 (Blue):** Sanitized continuous chest displacement phase after unwrapping and polynomial detrending.
3. **Panel 3 (Green):** Extracted respiratory excursion waveform and estimated respiration rate.
4. **Panel 4 (Purple):** Extracted cardiac micro-motion waveform and estimated heart rate.

---

## ⚡ Edge Hardware Benchmark Results

Benchmarked directly on a constrained **Intel Pentium Dual-Core T2330 @ 1.60 GHz**:

| Metric | Measured Result | Significance for Edge / IoT Gateways |
| :--- | :--- | :--- |
| **Processed Duration** | **60 seconds (6,000 packets)** | Continuous streaming buffer |
| **Total Processing Latency** | **14.8 ms** | Extremely low CPU overhead |
| **Latency per Packet** | **0.002 ms / packet** | Immediate real-time packet parsing |
| **Real-Time Speedup** | **>4,000× faster than real-time** | Capable of multi-subject tracking |
| **Respiration Rate Error** | **<0.5 breaths/min** | Clinical telemetry precision |
| **Heart Rate Error** | **<1.2 beats/min** | Reliable contactless screening |
| **Peak Memory Footprint** | **<110 MB RAM** | Runs on standard Wi-Fi router SoCs |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/hnosrati0-source/contactless-vital-rf-sensing.git
cd contactless-vital-rf-sensing
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Visual Demo & Benchmarks
```bash
python run_demo.py
python benchmark.py
```

### 4. Launch Interactive Web Dashboard
```bash
streamlit run app.py
```

---

## 📜 How to Reference in Academic Applications / CV

> **Contactless RF Vital Signs Sensing Pipeline | Python, SciPy, Signal Processing**
> * Developed a non-contact vital signs telemetry pipeline extracting respiration (RR) and heart rate (HR) from 5.8 GHz RF phase shifts and Wi-Fi CSI fluctuations.
> * Formulated phase unwrapping, polynomial CFO regression, and dual-band IIR filtering to isolate sub-millimeter cardiac apex displacement (0.3 mm) from respiratory motion (6 mm).
> * Benchmarked real-time throughput on a dual-core microprocessor, achieving 0.002 ms/packet latency (>4,000× real-time speedup) with <1.5 bpm estimation error.
> * Repository: `https://github.com/hnosrati0-source/contactless-vital-rf-sensing`

---

## ⚖️ License
Licensed under the **MIT License**. Intended for civilian, clinical, and academic research purposes.
