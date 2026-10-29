"""Unified Contactless RF Vital Sensing Pipeline."""

from typing import Dict, Any, Tuple
import numpy as np

from src.dsp.phase_sanitizer import sanitize_rf_phase
from src.dsp.vital_separator import extract_vital_waveforms
from src.features.estimator import estimate_vital_rates


class RFVitalSensingPipeline:
    def __init__(self, fs: float = 100.0, carrier_freq_ghz: float = 5.8):
        self.fs = fs
        self.carrier_freq_ghz = carrier_freq_ghz

    def process(self, raw_wrapped_phase: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict[str, float]]:
        # 1. Sanitize raw RF phase
        sanitized_phase = sanitize_rf_phase(raw_wrapped_phase, fs=self.fs)

        # 2. Separate respiration and heartbeat
        resp_wave, cardiac_wave = extract_vital_waveforms(sanitized_phase, fs=self.fs)

        # 3. Estimate rates
        metrics = estimate_vital_rates(resp_wave, cardiac_wave, fs=self.fs)

        return sanitized_phase, resp_wave, cardiac_wave, metrics

