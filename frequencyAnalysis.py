import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import find_peaks

def read_hex_file(file_path):
    """ Reads hex data from a text file and converts it to a signed 16-bit integer array. """
    data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)
    
    # Extract first 16-bit parts
    first_16_bits = data[0] + data[1]  # Concatenate first two hex values
    decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)
    
    return decimal_values

def compute_fft(signal, sampling_rate):
    """ Computes the FFT of the signal and returns frequencies and their magnitudes. """
    N = len(signal)  # Number of samples
    fft_values = fft(signal)  # Compute FFT
    fft_magnitudes = np.abs(fft_values)[:N // 2]  # Take magnitude of first half
    freqs = fftfreq(N, 1 / sampling_rate)[:N // 2]  # Compute frequency bins
    
    return freqs, fft_magnitudes

def analyze_signal(signal):
    """ Computes basic statistics and finds peaks in the signal. """
    mean_val = np.mean(signal)
    std_dev = np.std(signal)
    peaks, _ = find_peaks(signal, height=0)  # Find peaks
    
    return mean_val, std_dev, peaks

if __name__ == "__main__":
    # File path (replace with actual filename)
    FREQUENCY= "11"


    # Define file path
    file_path = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.10.txt" 
    # Sampling parameters
    sampling_rate = 1 / (200e-9)  # 5 MHz (since each step is 200 ns)

    # Read signal from hex file
    signal = read_hex_file(file_path)

    # Compute FFT and frequency analysis
    frequencies, magnitudes = compute_fft(signal, sampling_rate)

    # Find dominant frequency
    dominant_freq = frequencies[np.argmax(magnitudes)]
    print(f"Dominant Frequency: {dominant_freq:.2f} Hz")

    # Perform signal analysis
    mean_val, std_dev, peaks = analyze_signal(signal)
    print(f"Signal Mean: {mean_val:.2f}")
    print(f"Signal Standard Deviation: {std_dev:.2f}")
    print(f"Number of Peaks: {len(peaks)}")

    # Plot Time Domain Signal
    plt.figure(figsize=(12, 6))
    time_values = np.arange(len(signal)) * (1 / sampling_rate)
    plt.plot(time_values, signal, label="Original Signal", linewidth=1)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Time Domain Signal")
    plt.grid(True)
    plt.legend()
    # plt.savefig("../Testing/Experiment-1/10Khz/time_domain_signal.png", dpi=300)  # Save figure as an image
    plt.close()
    # plt.show()

    # Plot Frequency Spectrum
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, magnitudes, label="FFT Magnitude Spectrum", linewidth=1)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Frequency Spectrum")
    plt.grid(True)
    plt.legend()

    # Set limits and increments
    plt.xlim(990000, 1100000)  # 0 Hz to 1000 kHz

    plt.show()


    print("Plots saved as 'time_domain_signal.png' and 'frequency_spectrum.png'.")




# #########################################NEW################################################
# import numpy as np
# import pandas as pd
# from scipy.fftpack import fft, fftfreq
# from scipy.signal import find_peaks
# import os

# def read_hex_file(file_path):
#     """ Reads hex data from a text file and converts it to a signed 16-bit integer array. """
#     data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)

#     # Extract first 16-bit parts
#     first_16_bits = data[0] + data[1]  # Concatenate first two hex values
#     decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

#     return decimal_values

# def compute_fft(signal, sampling_rate):
#     """ Computes the FFT of the signal and returns frequencies and their magnitudes. """
#     N = len(signal)  # Number of samples
#     fft_values = fft(signal)  # Compute FFT
#     fft_magnitudes = np.abs(fft_values)[:N // 2]  # Take magnitude of first half
#     freqs = fftfreq(N, 1 / sampling_rate)[:N // 2]  # Compute frequency bins
    
#     return freqs, fft_magnitudes

# def analyze_signal(signal):
#     """ Computes basic statistics and finds peaks in the signal. """
#     mean_val = np.mean(signal)
#     std_dev = np.std(signal)
#     peaks, _ = find_peaks(signal, height=0)  # Find peaks
    
#     return mean_val, std_dev, len(peaks)

# def save_results_as_csv(results, output_file):
#     """ Saves analysis results into a structured CSV file. """
#     df = pd.DataFrame(results)
#     df.to_csv(output_file, index=False)
#     print(f"📁 Results saved in: {output_file}")

# if __name__ == "__main__":
#     # Define frequency range
#     frequencies = range(10, 1010, 10)  # 10 kHz to 1000 kHz with step of 10 kHz

#     # Define output file
#     output_file = "../Testing/Experiment-1/Analysis_Results/frequency_analysis_results_2.csv"
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists

#     # Define sampling parameters
#     sampling_rate = 1 / (200e-9)  # 5 MHz (since each step is 200 ns)

#     # Store results in a structured list
#     results = []

#     for freq in frequencies:
#         file_path = f"../Testing/Experiment-1/{freq}Khz/output_hex_data({freq}Khz)_192.168.1.20.txt"

#         if os.path.isfile(file_path):
#             print(f"✅ Processing: {file_path}")

#             # Read signal from hex file
#             signal = read_hex_file(file_path)

#             # Compute FFT and frequency analysis
#             freq_values, magnitudes = compute_fft(signal, sampling_rate)

#             # Find dominant frequency
#             dominant_freq = freq_values[np.argmax(magnitudes)]

#             # Perform signal analysis
#             mean_val, std_dev, num_peaks = analyze_signal(signal)

#             # Store results in table format
#             results.append({
#                 "Frequency (kHz)": freq,
#                 "Dominant Frequency (Hz)": round(dominant_freq, 2),
#                 "Signal Mean": round(mean_val, 4),
#                 "Signal Std Dev": round(std_dev, 4),
#                 "Number of Peaks": num_peaks
#             })
#         else:
#             print(f"⚠️ File not found: {file_path}")

#     # Save results to CSV
#     save_results_as_csv(results, output_file)
