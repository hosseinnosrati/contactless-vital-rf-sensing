"""Visual Demo: Contactless Vital Signs Sensing via RF Phase Processing.

Generates multi-stage signal decomposition figure comparing:
1. Raw Wrapped RF Phase (with simulated CFO drift)
2. Sanitized Chest Displacement Phase
3. Extracted Respiration Waveform & Rate
4. Extracted Cardiac Micro-Displacement Waveform & Rate
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.rf.csi_loader import generate_rf_vital_signal
from src.pipeline import RFVitalSensingPipeline


def run_demo():
    print("Running Contactless RF Vital Sensing Demo...")
    fs = 100.0
    duration = 20.0
    true_rr = 15.0  # 15 breaths/min
    true_hr = 70.0  # 70 beats/min

    t, raw_phase, gt = generate_rf_vital_signal(
        duration_sec=duration,
        fs=fs,
        carrier_freq_ghz=5.8,
        true_rr_bpm=true_rr,
        true_hr_bpm=true_hr,
        snr_db=16.0,
        inject_phase_drift=True
    )

    pipeline = RFVitalSensingPipeline(fs=fs, carrier_freq_ghz=5.8)
    sanitized, resp_wave, cardiac_wave, metrics = pipeline.process(raw_phase)

    print(f"Ground Truth: Respiration = {true_rr:.1f} bpm | Heart Rate = {true_hr:.1f} bpm")
    print(f"Estimated:    Respiration = {metrics['estimated_rr_bpm']:.1f} bpm | Heart Rate = {metrics['estimated_hr_bpm']:.1f} bpm")
    print(f"Error:        RR Error = {abs(metrics['estimated_rr_bpm'] - true_rr):.2f} bpm | HR Error = {abs(metrics['estimated_hr_bpm'] - true_hr):.2f} bpm")

    # Plotting 4-panel figure
    fig, axes = plt.subplots(4, 1, figsize=(13, 10), sharex=True)
    plt.subplots_adjust(hspace=0.3)

    # Panel 1: Raw Wrapped Phase
    axes[0].plot(t, raw_phase, color="#d9534f", lw=1.0)
    axes[0].set_title("Stage 1: Raw Wrapped RF CSI Phase (with CFO Carrier Drift & 2pi Jumps)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Phase (rad)")
    axes[0].grid(True, linestyle="--", alpha=0.5)

    # Panel 2: Sanitized Chest Displacement
    axes[1].plot(t, sanitized, color="#0275d8", lw=1.2)
    axes[1].set_title("Stage 2: Sanitized Chest Wall Phase (Unwrapped, Detrended & Denoised)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Phase (rad)")
    axes[1].grid(True, linestyle="--", alpha=0.5)

    # Panel 3: Respiration
    axes[2].plot(t, resp_wave, color="#28a745", lw=1.5, label="Filtered Respiration")
    axes[2].set_title(
        f"Stage 3: Extracted Respiration Waveform (Estimated: {metrics['estimated_rr_bpm']:.1f} bpm | True: {true_rr:.1f} bpm)",
        fontsize=11, fontweight="bold"
    )
    axes[2].set_ylabel("Amp (rad)")
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].legend(loc="upper right")

    # Panel 4: Cardiac Micro-displacement
    axes[3].plot(t, cardiac_wave, color="#6f42c1", lw=1.2, label="Cardiac Micro-Motion (Apex Beat)")
    axes[3].set_title(
        f"Stage 4: Extracted Cardiac Micro-Displacement (Estimated: {metrics['estimated_hr_bpm']:.1f} bpm | True: {true_hr:.1f} bpm)",
        fontsize=11, fontweight="bold"
    )
    axes[3].set_xlabel("Time (seconds)", fontsize=11)
    axes[3].set_ylabel("Amp (rad)")
    axes[3].grid(True, linestyle="--", alpha=0.5)
    axes[3].legend(loc="upper right")

    os.makedirs("assets", exist_ok=True)
    out_path = "assets/demo_vital_rf_sensing.png"
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Visual demo plot saved successfully to {out_path}!")


if __name__ == "__main__":
    run_demo()

