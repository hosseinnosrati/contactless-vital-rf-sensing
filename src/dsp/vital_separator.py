"""Vital Sign Separation Module.

Decomposes sanitized chest displacement phase into respiration and cardiac components.
"""

from typing import Tuple
import numpy as np
from scipy import signal


def extract_vital_waveforms(
    sanitized_phase: np.ndarray,
    fs: float = 100.0
) -> Tuple[np.ndarray, np.ndarray]:
    """Separates sanitized phase into respiration and cardiac waveforms.

    Parameters
    ----------
    sanitized_phase : np.ndarray
        Cleaned unwrapped phase.
    fs : float
        Sampling rate in Hz.

    Returns
    -------
    resp_waveform : np.ndarray (Respiration: 0.1 - 0.5 Hz)
    cardiac_waveform : np.ndarray (Heartbeat: 0.8 - 2.2 Hz)
    """
    nyq = 0.5 * fs

    # 1. Respiration Bandpass Filter (0.1 - 0.5 Hz)
    b_resp, a_resp = signal.butter(3, [0.1 / nyq, 0.5 / nyq], btype="band")
    resp_waveform = signal.filtfilt(b_resp, a_resp, sanitized_phase)

    # 2. Respiration Harmonic Suppression:
    # Subtract estimated respiration fundamental from phase before cardiac extraction
    residual_phase = sanitized_phase - resp_waveform

    # 3. Cardiac Bandpass Filter (0.8 - 2.2 Hz -> 48 to 132 bpm)
    b_cardiac, a_cardiac = signal.butter(4, [0.8 / nyq, 2.2 / nyq], btype="band")
    cardiac_waveform = signal.filtfilt(b_cardiac, a_cardiac, residual_phase)

    return resp_waveform, cardiac_waveform

