import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
FREQUENCY= "1"

# Load your signal (Example: Replace with actual data)
file_path = f"../Testing/Experiment-1/{FREQUENCY}Khz/output_hex_data({FREQUENCY}Khz)_192.168.1.10.txt"
data = pd.read_csv(file_path, sep='\s+', header=None, dtype=str)

# Extract first 16-bit parts
first_16_bits = data[0] + data[1]  # Concatenate first two hex values
decimal_values = np.array([int(x, 16) for x in first_16_bits]).astype(np.int16)

# Define parameters
  # Example: 5 kHz (Adjust based on your actual data)
time_step = 200e-9 # Time step per sample

# Generate time axis
time_values = np.arange(len(decimal_values)) * time_step

# Find fundamental period using peaks (assuming cyclic behavior)
threshold = 0.95 * np.max(decimal_values)  # Set threshold at 60% of max value
peaks, _ = find_peaks(decimal_values, height=threshold, distance=200)

# Estimate cycle length (period in samples)
cycle_lengths = np.diff(peaks)
average_cycle_length = int(np.mean(cycle_lengths))

# Reshape signal into cycles (truncate to match complete cycles)
num_cycles = len(decimal_values) // average_cycle_length
reshaped_signal = decimal_values[:num_cycles * average_cycle_length].reshape(num_cycles, average_cycle_length)

# Compute Time Synchronous Average
tsa_signal = np.mean(reshaped_signal, axis=0)

# Generate time axis for one cycle
tsa_time = np.linspace(0, average_cycle_length * time_step, average_cycle_length)

# Plot TSA result
plt.figure(figsize=(10, 5))
plt.plot(tsa_time, tsa_signal, label="Time Synchronous Average", linewidth=2)
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Time Synchronous Averaging (TSA)")
plt.grid(True)
plt.legend()
plt.show()
