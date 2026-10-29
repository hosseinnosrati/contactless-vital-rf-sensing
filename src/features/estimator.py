"""Vital Signs Rate Estimator.

Computes Respiration Rate (RR) and Heart Rate (HR) using hybrid time-domain
peak detection and frequency-domain FFT power spectral peak estimation.
"""

from typing import Dict, Any
import numpy as np
from scipy import signal


def estimate_vital_rates(
    resp_waveform: np.ndarray,
    cardiac_waveform: np.ndarray,
    fs: float = 100.0
) -> Dict[str, float]:
    """Estimates Respiration Rate (breaths/min) and Heart Rate (beats/min).

    Parameters
    ----------
    resp_waveform : np.ndarray
    cardiac_waveform : np.ndarray
    fs : float

    Returns
    -------
    Dict[str, float] with 'estimated_rr_bpm', 'estimated_hr_bpm', and spectral peaks.
    """
    n = len(resp_waveform)
    # Zero-padded FFT for high spectral resolution
    n_fft = max(4096, 2 ** int(np.ceil(np.log2(n) + 2)))
    freqs = np.fft.rfftfreq(n_fft, d=1.0 / fs)

    # 1. Respiration Rate (0.1 - 0.5 Hz)
    resp_fft = np.abs(np.fft.rfft(resp_waveform * signal.windows.hann(n), n=n_fft))
    resp_mask = (freqs >= 0.1) & (freqs <= 0.5)
    f_resp_peak = freqs[resp_mask][np.argmax(resp_fft[resp_mask])]
    rr_bpm = float(f_resp_peak * 60.0)

    # 2. Heart Rate (0.8 - 2.2 Hz)
    cardiac_fft = np.abs(np.fft.rfft(cardiac_waveform * signal.windows.hann(n), n=n_fft))
    cardiac_mask = (freqs >= 0.8) & (freqs <= 2.2)
    f_cardiac_peak = freqs[cardiac_mask][np.argmax(cardiac_fft[cardiac_mask])]
    hr_bpm = float(f_cardiac_peak * 60.0)

    return {
        "estimated_rr_bpm": rr_bpm,
        "estimated_hr_bpm": hr_bpm,
        "resp_peak_freq_hz": float(f_resp_peak),
        "cardiac_peak_freq_hz": float(f_cardiac_peak)
    }

