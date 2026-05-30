import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Replace with your actual CSV filename
filename = "phase_difference_data.csv"

# Read the CSV file
df = pd.read_csv(filename)

# Take the absolute value (modulus) of phase difference
df["Phase Difference (Degrees)"] = df["Phase Difference (Degrees)"].abs()

# Fit a linear trend line
z = np.polyfit(df["Frequency (kHz)"], df["Phase Difference (Degrees)"], 1)
p = np.poly1d(z)

# Plotting with colormap
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    df["Frequency (kHz)"],
    df["Phase Difference (Degrees)"],
    c=df["Frequency (kHz)"],   # Color by frequency
    cmap='viridis',            # You can try: 'plasma', 'cool', 'jet', 'inferno'
    edgecolor='k'
)

plt.plot(df["Frequency (kHz)"], p(df["Frequency (kHz)"]), color='red', linestyle='--', label="Trend Line")
plt.title("Phase Difference vs Frequency")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Phase Difference (Degrees)")
plt.grid(True)
plt.legend()
plt.colorbar(scatter, label="Frequency (kHz)")  # Add a color bar
plt.show()
