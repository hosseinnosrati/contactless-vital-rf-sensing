"""Contactless RF Vital Signs Web Dashboard.

Run via:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.rf.csi_loader import generate_rf_vital_signal
from src.pipeline import RFVitalSensingPipeline

st.set_page_config(page_title="Contactless RF Vital Signs", page_icon="📡", layout="wide")

st.title("📡 Contactless Vital Signs Sensing via RF & Wi-Fi CSI")
st.markdown(
    "**Non-Invasive Respiration & Heartbeat Telemetry** | "
    "*[GitHub Repository](https://github.com/hnosrati0-source/contactless-vital-rf-sensing)*"
)
st.caption("Extracts micro-Doppler chest displacements from wireless channel fluctuations without body contact.")

st.sidebar.header("⚙️ RF & Channel Parameters")
carrier_ghz = st.sidebar.selectbox("Carrier Frequency (GHz):", [5.8, 5.0, 2.4, 60.0], index=0)
duration = st.sidebar.slider("Observation Window (Seconds):", 10, 60, 20, 5)
snr_db = st.sidebar.slider("Channel SNR (dB):", 5.0, 30.0, 18.0, 1.0)
inject_drift = st.sidebar.checkbox("Simulate Oscillator CFO Drift", value=True)

st.sidebar.subheader("Subject Parameters")
sim_rr = st.sidebar.slider("Simulated Breathing Rate (bpm):", 8.0, 30.0, 16.0, 1.0)
sim_hr = st.sidebar.slider("Simulated Heart Rate (bpm):", 45.0, 120.0, 72.0, 1.0)

# Generate & Process
fs = 100.0
t, raw_phase, gt = generate_rf_vital_signal(
    duration_sec=duration,
    fs=fs,
    carrier_freq_ghz=carrier_ghz,
    true_rr_bpm=sim_rr,
    true_hr_bpm=sim_hr,
    snr_db=snr_db,
    inject_phase_drift=inject_drift
)

pipeline = RFVitalSensingPipeline(fs=fs, carrier_freq_ghz=carrier_ghz)
sanitized, resp, cardiac, metrics = pipeline.process(raw_phase)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Estimated Respiration", f"{metrics['estimated_rr_bpm']:.1f} bpm", delta=f"True: {sim_rr:.1f} bpm")
col2.metric("Estimated Heart Rate", f"{metrics['estimated_hr_bpm']:.1f} bpm", delta=f"True: {sim_hr:.1f} bpm")
col3.metric("Carrier Wavelength", f"{gt['wavelength_m']*100:.2f} cm")
col4.metric("Sampling Rate", f"{int(fs)} Hz")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 7), sharex=True)
plt.subplots_adjust(hspace=0.25)

ax1.plot(t, raw_phase, color="#d9534f", lw=1.0)
ax1.set_title("Raw Wrapped RF Phase with CFO Drift", fontweight="bold")
ax1.set_ylabel("Phase (rad)")
ax1.grid(True, linestyle="--", alpha=0.5)

ax2.plot(t, resp, color="#28a745", lw=1.4)
ax2.set_title(f"Extracted Respiration Motion ({metrics['estimated_rr_bpm']:.1f} breaths/min)", fontweight="bold")
ax2.set_ylabel("Amp (rad)")
ax2.grid(True, linestyle="--", alpha=0.5)

ax3.plot(t, cardiac, color="#6f42c1", lw=1.2)
ax3.set_title(f"Extracted Cardiac Apex Micro-Motion ({metrics['estimated_hr_bpm']:.1f} beats/min)", fontweight="bold")
ax3.set_xlabel("Time (seconds)")
ax3.set_ylabel("Amp (rad)")
ax3.grid(True, linestyle="--", alpha=0.5)

st.pyplot(fig)
