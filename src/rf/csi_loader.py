"""RF Channel State Information (CSI) & Radar Signal Generator.

Simulates multi-carrier wireless propagation influenced by micro-motions of the human chest:
- Static multipath reflections (walls, furniture).
- Dynamic chest displacement from respiration (~5-12 mm at 0.1-0.5 Hz).
- Micro-displacement from cardiac apex beat (~0.1-0.5 mm at 0.8-2.2 Hz).
- Hardware impairments: Carrier Frequency Offset (CFO) and phase noise.
"""

from typing import Tuple, Dict, Any
import numpy as np


def generate_rf_vital_signal(
    duration_sec: float = 30.0,
    fs: float = 100.0,
    carrier_freq_ghz: float = 5.8,
    true_rr_bpm: float = 16.0,
    true_hr_bpm: float = 72.0,
    snr_db: float = 18.0,
    inject_phase_drift: bool = True
) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """Synthesizes time-series RF complex CSI / phase data.

    Parameters
    ----------
    duration_sec : float
        Recording duration in seconds.
    fs : float
        Packet sampling rate in Hz (standard Wi-Fi CSI logging rate ~100 Hz).
    carrier_freq_ghz : float
        Carrier frequency in GHz (5.8 GHz standard ISM / Wi-Fi 5/6 band).
    true_rr_bpm : float
        Ground truth respiration rate in breaths per minute.
    true_hr_bpm : float
        Ground truth heart rate in beats per minute.
    snr_db : float
        Signal-to-noise ratio in decibels.
    inject_phase_drift : bool
        Simulate unsynchronized LO drift (linear CFO phase slope).

    Returns
    -------
    t : np.ndarray (time vector)
    csi_phase : np.ndarray (wrapped raw RF phase in radians)
    ground_truth : Dict[str, Any]
    """
    n_samples = int(duration_sec * fs)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    # Speed of light and RF wavelength
    c = 3e8
    wavelength_m = c / (carrier_freq_ghz * 1e9)  # ~0.0517 m for 5.8 GHz

    # 1. Respiration chest displacement (mm to meters)
    f_resp = true_rr_bpm / 60.0
    resp_amplitude_m = 0.006  # 6 mm
    resp_motion = resp_amplitude_m * np.sin(2 * np.pi * f_resp * t)

    # 2. Cardiac apex chest micro-displacement (mm to meters)
    f_cardiac = true_hr_bpm / 60.0
    cardiac_amplitude_m = 0.0003  # 0.3 mm (20x smaller than breathing)
    cardiac_motion = cardiac_amplitude_m * (
        np.sin(2 * np.pi * f_cardiac * t) + 0.3 * np.sin(4 * np.pi * f_cardiac * t)
    )

    total_displacement = resp_motion + cardiac_motion

    # 3. Two-way phase shift: Delta_phi = (4 * pi / lambda) * Delta_d
    clean_phase = (4.0 * np.pi / wavelength_m) * total_displacement

    # 4. Hardware impairments: static DC multipath + linear phase drift
    static_phase = 0.85
    cfo_slope = 0.45 * t if inject_phase_drift else 0.0

    raw_phase = clean_phase + static_phase + cfo_slope

    # 5. Add Gaussian noise
    signal_power = np.var(clean_phase)
    noise_power = signal_power / (10.0 ** (snr_db / 10.0))
    noise = np.random.normal(0, np.sqrt(noise_power), n_samples)
    noisy_phase = raw_phase + noise

    # Wrap to [-pi, pi] matching raw Wi-Fi CSI phase registers
    wrapped_phase = np.angle(np.exp(1j * noisy_phase))

    ground_truth = {
        "true_rr_bpm": true_rr_bpm,
        "true_hr_bpm": true_hr_bpm,
        "resp_motion_m": resp_motion,
        "cardiac_motion_m": cardiac_motion,
        "wavelength_m": wavelength_m
    }

    return t, wrapped_phase, ground_truth

