import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks

FREQUENCY = "100"  # Set desired frequency (change as needed)

# Define base directory
base_dir = f"../Testing/Experiment-1/{FREQUENCY}Khz/"

# Define board files with corresponding colors
board_files = {
    "Board1": {"path": f"{base_dir}output_hex_data({FREQUENCY}Khz)_192.168.1.10.txt", "color": "red"},
    "Board2": {"path": f"{base_dir}output_hex_data({FREQUENCY}Khz)_192.168.1.20.txt", "color": "green"},
}

# Output directory for saving graphs
output_dir = f"../Testing/Figures/Freq/{FREQUENCY}Khz/"
os.makedirs(output_dir, exist_ok=True)

# Sampling parameters
sampling_rate = 1 / (200e-9)  # 5 MHz (each step is 200 ns)

def read_hex_file(file_path):
    data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)
    first_16_bits = data[0] + data[1]
    decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)
    return decimal_values


def compute_fft(signal, sampling_rate):
    N = len(signal)
    signal = signal - np.mean(signal)
    # window = np.hamming(N)
    # signal *= window
    fft_values = fft(signal)
    fft_magnitudes = np.abs(fft_values[:N // 2]) #/ sum(window)
    fft_magnitudes_db = 20 * np.log10(fft_magnitudes + 1e-10)
    freqs = fftfreq(N, 1 / sampling_rate)[:N // 2]
    return freqs, fft_magnitudes_db


def analyze_signal(signal):
    mean_val = np.mean(signal)
    std_dev = np.std(signal)
    peak_threshold = 0.9 * np.max(signal)
    peaks, _ = find_peaks(signal, height=peak_threshold)
    return mean_val, std_dev, peaks


# Loop through each board and create separate FFT plots
for board_name, info in board_files.items():
    file_path = info["path"]
    color = info["color"]

    if os.path.isfile(file_path):
        print(f"✅ Processing: {file_path}")

        # Read signal from hex file
        signal = read_hex_file(file_path)

        # Compute FFT and frequency analysis
        frequencies, magnitudes_db = compute_fft(signal, sampling_rate)

        # Find dominant frequency
        dominant_freq = frequencies[np.argmax(magnitudes_db)]
        mean_val, std_dev, peaks = analyze_signal(signal)

        print(f"[{board_name}] Dominant Frequency: {dominant_freq:.2f} Hz")
        print(f"[{board_name}] Signal Mean: {mean_val:.2f}")
        print(f"[{board_name}] Signal Standard Deviation: {std_dev:.2f}")
        print(f"[{board_name}] Number of Peaks (90% Max): {len(peaks)}")

        # Plot frequency spectrum
        plt.figure(figsize=(12, 6))
        plt.plot(*compute_fft(signal, sampling_rate), label="FFT Magnitude Spectrum (dB)", linewidth=1, color=color)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude (dB)")
        plt.title(f"Frequency Spectrum - {FREQUENCY} kHz - {color.capitalize()} - {board_name}")
        plt.grid(True)
        plt.xlim([99000,101000])
        plt.ylim(bottom=150)
        plt.legend()

        # Save the plot separately
        output_file = f"{output_dir}{FREQUENCY}Khz_FFT_{color}_{board_name}.png"
        plt.savefig(output_file, dpi=300)
        plt.close()

    else:
        print(f"❌ File not found: {file_path}")
