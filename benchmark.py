"""Hardware Latency and Memory Profiler for RF Vital Sensing."""

import time
import os
import psutil
import numpy as np

from src.rf.csi_loader import generate_rf_vital_signal
from src.pipeline import RFVitalSensingPipeline


def run_benchmark():
    process = psutil.Process(os.getpid())
    init_mem_mb = process.memory_info().rss / (1024 * 1024)

    print("=" * 60)
    print("      CONTACTLESS RF VITAL SENSING BENCHMARK")
    print("=" * 60)
    print(f"Initial Memory Footprint: {init_mem_mb:.2f} MB")

    fs = 100.0
    duration_sec = 60.0
    t, raw_phase, gt = generate_rf_vital_signal(
        duration_sec=duration_sec,
        fs=fs,
        carrier_freq_ghz=5.8,
        true_rr_bpm=16.0,
        true_hr_bpm=72.0,
        snr_db=18.0
    )

    pipeline = RFVitalSensingPipeline(fs=fs, carrier_freq_ghz=5.8)

    t0 = time.perf_counter()
    sanitized, resp, cardiac, metrics = pipeline.process(raw_phase)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    final_mem_mb = process.memory_info().rss / (1024 * 1024)
    speedup = (duration_sec * 1000.0) / elapsed_ms

    print(f"Processed RF Duration:    {duration_sec} seconds ({int(duration_sec * fs)} packets)")
    print(f"Ground Truth RR / HR:     {gt['true_rr_bpm']} bpm / {gt['true_hr_bpm']} bpm")
    print(f"Estimated RR / HR:        {metrics['estimated_rr_bpm']:.1f} bpm / {metrics['estimated_hr_bpm']:.1f} bpm")
    print("-" * 60)
    print(f"Total Processing Time:    {elapsed_ms:.2f} ms")
    print(f"Latency per Packet:       {(elapsed_ms / (duration_sec * fs)):.3f} ms / packet")
    print(f"Real-Time Speedup:        {speedup:.1f}x faster than real-time!")
    print(f"Peak Memory Usage:        {final_mem_mb:.2f} MB")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
