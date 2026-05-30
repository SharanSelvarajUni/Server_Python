import numpy as np
import matplotlib.pyplot as plt

# Define file parameters
file_path = "./ClientData_192.168.1.10.bin"
num_points = 5000000  # 5 million data points
dtype = np.float32  # Change to np.int32 if your data is integers
sampling_rate = 5000000  # 5 MHz (5M samples per second)
duration = num_points / sampling_rate  # Should be 1 second

# Load binary data
data = np.fromfile(file_path, dtype=dtype)

# Generate time array (0 to 1 sec)
time = np.linspace(0, duration, num_points, endpoint=False)

# Plot the data with time on x-axis
plt.figure(figsize=(12, 6))
plt.plot(time, data, linewidth=0.5)  # Thin line for performance
plt.title("Binary Data Plot")
plt.xlabel("Time (seconds)")  # X-axis in seconds
plt.ylabel("Value")
plt.grid(True)

# Show the plot
plt.show()
