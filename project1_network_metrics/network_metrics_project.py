import pandas as pd

# Read the data
df = pd.read_csv("network_metrics_project1.csv")

# Find problem devices
problem_devices = df[(df["latency_ms"] > 100) & (df["errors"] > 2)]

# Sort worst devices by latency
problem_devices_sorted = problem_devices.sort_values(by="latency_ms", ascending=False)

# Count total problem devices
total_problems = len(problem_devices)

# Group by region
problems_by_region = problem_devices.groupby("region")["errors"].sum()

# Print summary
print("=== Network Health Summary ===")
print(f"Total problem devices: {total_problems}")
print("\nTop 10 worst devices by latency:")
print(problem_devices_sorted[["device", "region", "latency_ms", "errors"]].head(10))

print("\nErrors by region:")
print(problems_by_region)

# Export report
problem_devices_sorted.to_csv("problem_devices_report.csv", index=False)

print("\nReport saved as problem_devices_report.csv")

