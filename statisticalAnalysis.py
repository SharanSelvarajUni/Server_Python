# import os
# import re
# import numpy as np
# import scipy.stats as stats
# import matplotlib.pyplot as plt

# # Set the base directory containing all frequency folders
# base_directory = r"C:\Users\mitarbeiter\Desktop\Testing\Experiment-1"  # Adjust to actual data path

# # List to store phase differences
# all_phase_differences = []
# phase_data_by_frequency = {}

# # Ensure base directory exists
# if not os.path.exists(base_directory):
#     print(f"ERROR: Base directory '{base_directory}' does not exist!")
#     exit()

# # Loop through each frequency folder
# for folder in sorted(os.listdir(base_directory)):
#     folder_path = os.path.join(base_directory, folder)

#     # Ensure it's a directory
#     if os.path.isdir(folder_path):
#         # Look for "synchronization_analysis" file (with or without .txt extension)
#         possible_files = ["synchronization_analysis", "synchronization_analysis.txt"]
#         sync_file_path = None

#         for filename in possible_files:
#             file_path = os.path.join(folder_path, filename)
#             if os.path.isfile(file_path):
#                 sync_file_path = file_path
#                 break  # Found file, exit loop

#         if sync_file_path:
#             print(f"✅ Found file: {sync_file_path}")
#         else:
#             print(f"⚠️ Missing file in: {folder_path}")
#             continue  # Skip this folder

#         # Extract phase difference
#         phase_differences = []
#         with open(sync_file_path, 'r') as file:
#             for line in file:
#                 match = re.search(r"Phase Difference \(degrees\): (-?\d+\.\d+)", line)
#                 if match:
#                     phase_differences.append(float(match.group(1)))

#         # Store extracted phase differences
#         if phase_differences:
#             phase_data_by_frequency[folder] = phase_differences
#             all_phase_differences.extend(phase_differences)

# # Debugging: Check collected data
# if not all_phase_differences:
#     print("No phase difference data found! Check file paths and file extensions.")
#     exit()

# # Convert to NumPy array
# all_phase_differences = np.array(all_phase_differences)

# # Compute statistics
# mean_phase = np.mean(all_phase_differences)
# std_dev = np.std(all_phase_differences, ddof=1)
# n = len(all_phase_differences)

# # 95% Confidence Interval Calculation
# confidence = 0.95
# z_value = stats.t.ppf((1 + confidence) / 2, df=n-1)
# margin_of_error = z_value * (std_dev / np.sqrt(n))

# # Confidence Interval Bounds
# lower_bound = mean_phase - margin_of_error
# upper_bound = mean_phase + margin_of_error

# # Print statistical summary
# print("\n---- Phase Difference Statistical Analysis ----")
# print(f"Total Measurements: {n}")
# print(f"Mean Phase Difference: {mean_phase:.4f}°")
# print(f"Standard Deviation: {std_dev:.4f}°")
# print(f"95% Confidence Interval: ({lower_bound:.4f}°, {upper_bound:.4f}°)")

# # Interpretation
# if lower_bound <= 0 <= upper_bound:
#     print("✅ The confidence interval includes 0°, suggesting no significant phase difference.")
# else:
#     print("⚠️ The confidence interval does NOT include 0°, suggesting a possible phase shift.")

# # ----- PLOTTING -----

# # # 1️⃣ HISTOGRAM with NORMAL DISTRIBUTION CURVE
# # plt.figure(figsize=(10, 5))
# # bins = 20  # Number of bins in histogram
# # plt.hist(all_phase_differences, bins=bins, density=True, edgecolor="black", alpha=0.7, label="Histogram")

# # # Generate Normal Distribution Curve
# # x_values = np.linspace(min(all_phase_differences), max(all_phase_differences), 100)
# # pdf_values = stats.norm.pdf(x_values, mean_phase, std_dev)
# # plt.plot(x_values, pdf_values, color='red', linewidth=2, label="Normal Distribution")

# # plt.axvline(x=mean_phase, color='blue', linestyle='--', label=f"Mean = {mean_phase:.2f}°")
# # plt.xlabel("Phase Difference (Degrees)")
# # plt.ylabel("Density")
# # plt.title("Histogram of Phase Differences with Normal Distribution")
# # plt.legend()
# # plt.grid()
# # plt.show()

# # 2️⃣ SCATTER PLOT: Phase Difference per Frequency (Sorted)
# plt.figure(figsize=(10, 5))

# # Extract numeric frequency values and sort
# sorted_frequencies = sorted(phase_data_by_frequency.keys(), key=lambda x: int(x.replace("Khz", "")))

# for freq in sorted_frequencies:
#     freq_numeric = int(freq.replace("Khz", ""))  # Convert to integer for plotting
#     plt.scatter([freq_numeric] * len(phase_data_by_frequency[freq]), 
#                 phase_data_by_frequency[freq], label=f"{freq}")

# plt.axhline(y=0, color='r', linestyle='--', label="Zero Phase Difference")
# plt.xlabel("Frequency (kHz)")
# plt.ylabel("Phase Difference (Degrees)")
# plt.title("Phase Difference Across Frequencies")
# plt.ylim(-10,10)
# plt.xticks(rotation=45)
# # plt.legend()
# plt.grid()
# plt.show()

import os
import re
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

# Set the base directory containing all frequency folders
base_directory = r"C:\Users\mitarbeiter\Desktop\Testing\Experiment-1"  # Adjust to actual data path

# List to store phase differences
all_phase_differences = []
phase_data_by_frequency = {}

# Ensure base directory exists
if not os.path.exists(base_directory):
    print(f"ERROR: Base directory '{base_directory}' does not exist!")
    exit()

# Loop through each frequency folder
for folder in sorted(os.listdir(base_directory)):
    folder_path = os.path.join(base_directory, folder)

    # Ensure it's a directory
    if os.path.isdir(folder_path):
        # Look for "synchronization_analysis" file (with or without .txt extension)
        possible_files = ["synchronization_analysis", "synchronization_analysis.txt"]
        sync_file_path = None

        for filename in possible_files:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                sync_file_path = file_path
                break  # Found file, exit loop

        if sync_file_path:
            print(f"✅ Found file: {sync_file_path}")
        else:
            print(f"⚠️ Missing file in: {folder_path}")
            continue  # Skip this folder

        # Extract phase difference
        phase_differences = []
        with open(sync_file_path, 'r') as file:
            for line in file:
                match = re.search(r"Phase Difference \(degrees\): (-?\d+\.\d+)", line)
                if match:
                    phase_differences.append(float(match.group(1)))

        # Store extracted phase differences
        if phase_differences:
            phase_data_by_frequency[folder] = phase_differences
            all_phase_differences.extend(phase_differences)

# Debugging: Check collected data
if not all_phase_differences:
    print("No phase difference data found! Check file paths and file extensions.")
    exit()

# Convert to NumPy array
all_phase_differences = np.array(all_phase_differences)

# Compute statistics
mean_phase = np.mean(all_phase_differences)
std_dev = np.std(all_phase_differences, ddof=1)
n = len(all_phase_differences)

# 95% Confidence Interval Calculation
confidence = 0.95
z_value = stats.t.ppf((1 + confidence) / 2, df=n-1)
margin_of_error = z_value * (std_dev / np.sqrt(n))

# Confidence Interval Bounds
lower_bound = mean_phase - margin_of_error
upper_bound = mean_phase + margin_of_error

# Print statistical summary
print("\n---- Phase Difference Statistical Analysis ----")
print(f"Total Measurements: {n}")
print(f"Mean Phase Difference: {mean_phase:.4f}°")
print(f"Standard Deviation: {std_dev:.4f}°")
print(f"95% Confidence Interval: ({lower_bound:.4f}°, {upper_bound:.4f}°)")

# Interpretation
if lower_bound <= 0 <= upper_bound:
    print("✅ The confidence interval includes 0°, suggesting no significant phase difference.")
else:
    print("⚠️ The confidence interval does NOT include 0°, suggesting a possible phase shift.")

# ----- SAVE DATA AS TABLE -----
# Convert data to pandas DataFrame
phase_diff_data = []

# Extract numeric frequency values and sort
sorted_frequencies = sorted(phase_data_by_frequency.keys(), key=lambda x: int(x.replace("Khz", "")))

for freq in sorted_frequencies:
    freq_numeric = int(freq.replace("Khz", ""))  # Convert to integer for sorting
    for phase_value in phase_data_by_frequency[freq]:
        phase_diff_data.append([freq_numeric, phase_value])

# Create DataFrame
df_phase_diff = pd.DataFrame(phase_diff_data, columns=["Frequency (kHz)", "Phase Difference (Degrees)"])

# Save to CSV
csv_filename = "phase_difference_data.csv"
df_phase_diff.to_csv(csv_filename, index=False)
print(f"✅ Phase difference data saved as '{csv_filename}'")

# ----- PLOTTING -----
plt.figure(figsize=(10, 5))

for freq in sorted_frequencies:
    freq_numeric = int(freq.replace("Khz", ""))  # Convert to integer for plotting
    plt.scatter([freq_numeric] * len(phase_data_by_frequency[freq]), 
                phase_data_by_frequency[freq], label=f"{freq}")

plt.axhline(y=0, color='r', linestyle='--', label="Zero Phase Difference")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Phase Difference (Degrees)")
plt.title("Phase Difference Across Frequencies")
plt.ylim(-7, 7)
plt.xticks(rotation=45)
plt.grid()
plt.show()
