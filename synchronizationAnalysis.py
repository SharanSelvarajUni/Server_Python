# import numpy as np
# import pandas as pd
# import sys
# from scipy.fftpack import fft, fftfreq
# from scipy.signal import find_peaks, correlate


# def read_hex_file(file_path, max_samples=200000):
#     """ Reads hex data from a text file and converts it to a signed 16-bit integer array. """
#     data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)
#     first_16_bits = data[0] + data[1]  # Concatenate first two hex values
#     decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

#     return decimal_values[:max_samples]  # Limit data size for faster processing


# def compute_fft(signal, sampling_rate, downsample_factor=10):
#     """ Computes FFT of downsampled signal for efficiency. """
#     # signal = signal[::downsample_factor]  # Downsample
#     N = len(signal)
#     fft_values = fft(signal)
#     magnitudes = np.abs(fft_values)[:N // 2]
#     freqs = fftfreq(N, 1 / sampling_rate)[:N // 2]
#     return freqs, magnitudes, fft_values[:N // 2]

# def analyze_synchronization(signal1, signal2, sampling_rate, output_file):
#     """ Computes cross-correlation and phase difference to check synchronization. Saves results to a file. """
#     with open(output_file, "w") as f:
#         # Ensure both signals are the same length
#         min_length = min(len(signal1), len(signal2))
#         signal1, signal2 = signal1[:min_length], signal2[:min_length]

#         # Compute FFT for both signals (with downsampling)
#         freqs1, magnitudes1, fft_values1 = compute_fft(signal1, sampling_rate)
#         freqs2, magnitudes2, fft_values2 = compute_fft(signal2, sampling_rate)

#         # Find dominant frequency
#         dominant_freq1 = freqs1[np.argmax(magnitudes1)]
#         dominant_freq2 = freqs2[np.argmax(magnitudes2)]

#         # Compute phase difference at dominant frequency
#         index1 = np.argmax(magnitudes1)
#         index2 = np.argmax(magnitudes2)
#         phase_diff = np.angle(fft_values1[index1]) - np.angle(fft_values2[index2])

#         # **Fast** FFT-based cross-correlation
#         cross_corr = correlate(signal1 - np.mean(signal1), signal2 - np.mean(signal2), mode='full', method='fft')
#         lag_at_max_corr = (np.argmax(cross_corr) - (min_length - 1)) * (1 / sampling_rate)

#         # Write results to file
#         f.write("--- Synchronization Analysis ---\n")
#         f.write(f"Dominant Frequency of Signal 1: {dominant_freq1:.2f} Hz\n")
#         f.write(f"Dominant Frequency of Signal 2: {dominant_freq2:.2f} Hz\n")
#         f.write(f"Phase Difference (radians): {phase_diff:.4f}\n")
#         f.write(f"Phase Difference (degrees): {np.degrees(phase_diff):.2f}°\n")
#         # f.write(f"Lag at Max Correlation: {lag_at_max_corr:.9f} seconds\n")
#         # f.write(f"Are signals synchronized? {'Yes' if abs(lag_at_max_corr) < (1 / dominant_freq1) else 'No'}\n")

# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python synchronization_analysis.py <hex_file_1> <hex_file_2> <output_file>")
#     else:
#         file1, file2, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
#         sampling_rate = 1 / (200e-9)  # 5 MHz
        
#         signal1 = read_hex_file(file1)
#         signal2 = read_hex_file(file2)
        
#         if signal1 is not None and signal2 is not None:
#             analyze_synchronization(signal1, signal2, sampling_rate, output_file)
#             print(f"Analysis saved to {output_file}")
#         else:
#             print("Error: Could not load one or both files. Check file paths.")


###################################################################################################################################

import numpy as np
import pandas as pd
import sys
import os
from scipy.fftpack import fft, fftfreq
from scipy.signal import correlate


def read_hex_file(file_path, max_samples=200000):
    """ Reads hex data from a text file and converts it to a signed 16-bit integer array. """
    try:
        data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)
        first_16_bits = data[0] + data[1]  # Concatenate first two hex values
        decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)
        return decimal_values[:max_samples]  # Limit data size for faster processing
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def compute_fft(signal, sampling_rate):
    """ Computes FFT and returns frequencies, magnitudes, and FFT complex values. """
    N = len(signal)
    fft_values = fft(signal)
    magnitudes = np.abs(fft_values)[:N // 2]
    freqs = fftfreq(N, 1 / sampling_rate)[:N // 2]
    return freqs, magnitudes, fft_values[:N // 2]


def analyze_synchronization(signal1, signal2, sampling_rate, freq, excel_writer):
    """ Computes synchronization analysis and writes results to an Excel file. """
    # Ensure both signals have the same length
    min_length = min(len(signal1), len(signal2))
    signal1, signal2 = signal1[:min_length], signal2[:min_length]

    # Compute FFT for both signals
    freqs1, magnitudes1, fft_values1 = compute_fft(signal1, sampling_rate)
    freqs2, magnitudes2, fft_values2 = compute_fft(signal2, sampling_rate)

    # Find dominant frequency
    dominant_freq1 = freqs1[np.argmax(magnitudes1)]
    dominant_freq2 = freqs2[np.argmax(magnitudes2)]

    # Compute phase difference at dominant frequency
    index1 = np.argmax(magnitudes1)
    index2 = np.argmax(magnitudes2)
    phase_diff = np.angle(fft_values1[index1]) - np.angle(fft_values2[index2])

    # Cross-correlation for time shift analysis
    cross_corr = correlate(signal1 - np.mean(signal1), signal2 - np.mean(signal2), mode='full', method='fft')
    lag_at_max_corr = (np.argmax(cross_corr) - (min_length - 1)) * (1 / sampling_rate)

    # Prepare data for Excel
    df = pd.DataFrame({
        "Frequency (Hz)": freqs1,
        "Magnitude Signal 1": magnitudes1,
        "Magnitude Signal 2": magnitudes2
    })

    # Summary table
    summary_data = {
        "Frequency (kHz)": [freq],
        "Dominant Freq 1 (Hz)": [dominant_freq1],
        "Dominant Freq 2 (Hz)": [dominant_freq2],
        "Phase Diff (radians)": [round(phase_diff,2)],
        "Phase Diff (degrees)": [round(np.degrees(phase_diff),1)],
        # "Lag at Max Corr (s)": [lag_at_max_corr]
    }
    summary_df = pd.DataFrame(summary_data)

    # Save both data and summary to different sheets
    df.to_excel(excel_writer, sheet_name=f"{freq}kHz_FFT", index=False)
    summary_df.to_excel(excel_writer, sheet_name=f"{freq}kHz_Summary", index=False)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python synchronization_analysis.py <hex_file_1> <hex_file_2> <output_directory>")
    else:
        file1, file2, output_dir = sys.argv[1], sys.argv[2], sys.argv[3]
        sampling_rate = 1 / (200e-9)  # 5 MHz
        frequency = os.path.basename(file1).split('_')[2].replace("Khz", "")

        # Create the Excel file in the specified directory
        excel_path = os.path.join(output_dir, "synchronization_analysis.xlsx").replace("\\", "/")
        excel_writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')

        # Read signals
        signal1 = read_hex_file(file1)
        signal2 = read_hex_file(file2)

        if signal1 is not None and signal2 is not None:
            analyze_synchronization(signal1, signal2, sampling_rate, frequency, excel_writer)
            excel_writer._save()
            print(f"Analysis saved to {excel_path}")
        else:
            print("❌ Error: Could not load one or both files. Check file paths.")
