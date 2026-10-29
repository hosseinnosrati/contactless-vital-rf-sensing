"""RF Phase Sanitization and Denoising Module.

Removes 2pi wrap discontinuities and oscillator Carrier Frequency Offset (CFO)
linear phase slopes from raw Wi-Fi CSI / radar phase measurements.
"""

import numpy as np
from scipy import signal


def sanitize_rf_phase(wrapped_phase: np.ndarray, fs: float = 100.0) -> np.ndarray:
    """Unwraps and detrends RF phase time-series.

    Parameters
    ----------
    wrapped_phase : np.ndarray
        Raw phase array wrapped to [-pi, pi].
    fs : float
        Sampling frequency in Hz.

    Returns
    -------
    sanitized_phase : np.ndarray
        Continuous unwrapped and detrended phase proportional to chest displacement.
    """
    # 1. Phase unwrapping
    unwrapped = np.unwrap(wrapped_phase)

    # 2. Linear / polynomial detrending to remove low-frequency oscillator drift (CFO)
    # Using low-order polynomial subtraction
    n_samples = len(unwrapped)
    x = np.linspace(-1, 1, n_samples)
    poly_coeffs = np.polyfit(x, unwrapped, deg=2)
    trend = np.polyval(poly_coeffs, x)
    detrended = unwrapped - trend

    # 3. Median filter to eliminate burst spikes (Hampel filter approximation)
    kernel_size = 5
    cleaned = signal.medfilt(detrended, kernel_size=kernel_size)

    return cleaned
