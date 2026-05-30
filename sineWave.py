import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Simulation parameters
Fs = 5000000  # Sampling rate: 5 MHz
T = 1 / Fs  # Sampling period
N = 500000  # Number of samples
f_sine = 10000  # Frequency of sine wave (10 kHz)

# Time vector
t = np.linspace(0, (N-1)*T, N)

# Generate sine wave (zero mean)
sine_wave = np.sin(2 * np.pi * f_sine * t)  

# Compute FFT
fft_values = fft(sine_wave)
fft_magnitude = np.abs(fft_values) / N  # Normalize
freqs = fftfreq(N, T)  # Frequency bins

# Plot FFT
plt.figure(figsize=(10, 5))
plt.plot(freqs[:N//2], fft_magnitude[:N//2])  # Plot only positive frequencies
plt.title("FFT of Simulated 10 kHz Sine Wave")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.xlim([0, 50000])  # Show up to 50 kHz
plt.show()
