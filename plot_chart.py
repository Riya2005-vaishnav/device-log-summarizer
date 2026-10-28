
import json
import matplotlib.pyplot as plt

# Load data from output.json
try:
    with open("output.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: output.json was not found. Please place it in the current folder.")
    raise SystemExit(1)

# Extract device IDs and average temperatures
device_ids = [item["device_id"] for item in data]
avg_temperatures = [item["avg_temperature"] for item in data]

# Create the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(device_ids, avg_temperatures)

# Add exact values above each bar
plt.bar_label(bars, fmt="%.2f", padding=3)

# Add chart labels and title
plt.xlabel("Device ID")
plt.ylabel("Average Temperature (°C)")
plt.title("Average Temperature per Device")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the chart
plt.savefig("chart.png", dpi=300, bbox_inches="tight")
plt.close()

print("Bar chart saved successfully as chart.png")
