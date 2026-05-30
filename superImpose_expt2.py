import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
# output_dir = f"../Testing/Figures/Freq/{FREQUENCY}Khz/"

number=1
# Define file path
file1 = f"../Testing/Experiment-2/Sensor{number}_excitation/output_hex_data_192.168.1.10.txt"
file2 = f"../Testing/Experiment-2/Sensor{number}_excitation/output_hex_data_192.168.1.20.txt"
file3 = f"../Testing/Experiment-2/Sensor{number}_excitation/output_hex_data_192.168.1.30.txt"
file4 = f"../Testing/Experiment-2/Sensor{number}_excitation/output_hex_data_192.168.1.40.txt"
# file1 = "output_hex_data(10hz).txt"  # Replace with actual filename
# file2 = "output_hex_data(5hz).txt"  # Replace with actual filename

# Parameters
window_size = 1  # Moving average window size
time_step = 200e-9  # 200 nanoseconds per step

# Read and process first file
data1 = pd.read_csv(file1, sep='\s+', header=None, dtype=str)
first_16_bits1 = data1[0] + data1[1]  # Concatenate first two hex values
decimal_values1 = np.array([int(x, 16) for x in first_16_bits1]).astype(np.int16)
voltage_values1 = ((decimal_values1 / 32767) * 5) + 0.8 # Convert to voltage range 
time_values1 = np.arange(len(voltage_values1)) * time_step
smoothed_values1 = np.convolve(voltage_values1, np.ones(window_size)/window_size, mode='same')
time_values1 = time_values1[:len(smoothed_values1)]

# Read and process second file
data2 = pd.read_csv(file2, sep='\s+', header=None, dtype=str)
first_16_bits2 = data2[0] + data2[1]  # Concatenate first two hex values
decimal_values2 = np.array([int(x, 16) for x in first_16_bits2]).astype(np.int16)
voltage_values2 = (decimal_values2 / 32767) * 5  # Convert to voltage range
time_values2 = np.arange(len(voltage_values2)) * time_step
smoothed_values2 = np.convolve(voltage_values2, np.ones(window_size)/window_size, mode='same')
time_values2 = time_values2[:len(smoothed_values2)]

# Read and process second file
data3 = pd.read_csv(file3, sep='\s+', header=None, dtype=str)
first_16_bits3 = data3[0] + data3[1]  # Concatenate first two hex values
decimal_values3 = np.array([int(x, 16) for x in first_16_bits3]).astype(np.int16)
voltage_values3 = ((decimal_values3 / 32767) * 5 ) + 0.8 # Convert to voltage range
time_values3 = np.arange(len(voltage_values3)) * time_step
smoothed_values3 = np.convolve(voltage_values3, np.ones(window_size)/window_size, mode='same')
time_values3 = time_values3[:len(smoothed_values3)]

# # Read and process second file
data4 = pd.read_csv(file4, sep='\s+', header=None, dtype=str)
first_16_bits4 = data4[0] + data4[1]  # Concatenate first two hex values
decimal_values4 = np.array([int(x, 16) for x in first_16_bits4]).astype(np.int16)
voltage_values4 = ((decimal_values4 / 32767) * 5)   # Convert to voltage range
time_values4 = np.arange(len(voltage_values4)) * time_step
smoothed_values4 = np.convolve(voltage_values4, np.ones(window_size)/window_size, mode='same')
time_values4 = time_values4[:len(smoothed_values4)]

# fifteenth_bit_values = ((decimal_values4 >> 14) & 1) * 3  # Shift and mask to get the 15th bit, map 1 -> 5V, 0 -> 0V


# Plot the superimposed graphs
plt.figure(figsize=(12, 6))
plt.plot(time_values1, voltage_values1, label='Top-Sensor-1', linewidth=1.5)
plt.plot(time_values2, voltage_values2, label='Top-Sensor-2', linewidth=1.5,color='black')
plt.plot(time_values3, voltage_values3, label='Bottom-Sensor-2', linewidth=1.5, color='green')
plt.plot(time_values4, voltage_values4, label='Bottom-Sensor-1', linewidth=1.5, color='red')
# plt.plot(time_values4, fifteenth_bit_values, label='Trigger signal', linewidth=1.5, color='black')

plt.xlabel("Time (seconds)")
plt.ylabel("Decimal Value")
plt.title("Superimposed Smoothed 16-bit Values over Time")
plt.legend()
plt.grid(True)

# Set axis ranges   
# plt.ylim([1.5, 1.8])  
plt.ylim([1.5, 1.8])
# plt.ylim([5, 5])
# plt.xlim([0, max(max(time_values1), max(time_values2), max(time_values3))])
# plt.xlim(1.27292, 1.27304) # Sensor:2
plt.xlim(2.00970, 2.00985)
# plt.xlim(1.8, 2.2)

# Save the plot separately
# output_file = f"{output_dir}{FREQUENCY}_superimposed.png"
# plt.savefig(output_file, dpi=300)

plt.show()  # Close figure to prevent display

# print(len(decimal_values1))
# print(len(decimal_values2))
