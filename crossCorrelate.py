import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_hex_file(file_path):
    """ Reads hex data from a text file and converts it to a signed 16-bit integer array. """
    data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)
    
    # Extract first 16-bit parts
    first_16_bits = data[0] + data[1]  # Concatenate first two hex values
    decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)
    
    return decimal_values

# File paths (replace with actual filenames)
file1 = "output_hex_data(10Khz)_192.168.1.10.txt"
file2 = "output_hex_data(10Khz)_192.168.1.20.txt"  # Second file for comparison

# Read data from both files
signal1 = read_hex_file(file1)
signal2 = read_hex_file(file2)

# Ensure both signals are the same length (truncate the longer one)
min_length = min(len(signal1), len(signal2))
signal1 = signal1[:min_length]
signal2 = signal2[:min_length]

# Compute cross-correlation
cross_corr = np.correlate(signal1 - np.mean(signal1), signal2 - np.mean(signal2), mode='full')

# Generate lag values (time shifts)
lags = np.arange(-min_length + 1, min_length) * 200e-9  # Convert to seconds

print(cross_corr)
print(lags)
# # Plot the cross-correlation
# plt.figure(figsize=(12, 6))
# plt.plot(lags, cross_corr, label="Cross-Correlation", linewidth=1.5)
# plt.xlabel("Time Lag (seconds)")
# plt.ylabel("Correlation")
# plt.title("Cross-Correlation of Two Signals")
# plt.axvline(x=0, color='r', linestyle='--', label="Zero Lag")
# plt.grid(True)
# plt.legend()

# plt.show()
