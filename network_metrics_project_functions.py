import pandas as pd

def load_data(file_name):
    return pd.read_csv(file_name)

def find_problem_devices(df):
    return df[(df["latency_ms"] > 100) & (df["errors"] > 2)]

def summarize_problems(problem_devices):
    total_problems = len(problem_devices)
    problems_by_region = problem_devices.groupby("region")["errors"].sum()
    return total_problems, problems_by_region

def save_report(problem_devices):
    problem_devices.to_csv("problem_devices_report.csv", index=False)

def main():
    df = load_data("C:/Users/19086/Downloads/network_metrics_project1.csv")
    problem_devices = find_problem_devices(df)
    problem_devices_sorted = problem_devices.sort_values(by="latency_ms", ascending=False)

    total_problems, problems_by_region = summarize_problems(problem_devices)

    print("=== Network Health Summary ===")
    print(f"Total problem devices: {total_problems}")
    print("\nTop 10 worst devices by latency:")
    print(problem_devices_sorted[["device", "region", "latency_ms", "errors"]].head(10))

    print("\nErrors by region:")
    print(problems_by_region)

    save_report(problem_devices_sorted)
    print("\nReport saved as problem_devices_report.csv")

if __name__ == "__main__":
    main()


