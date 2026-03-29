import pandas as pd

def get_network_api_data():
    return [
        {"device": "router1", "region": "nj1", "latency_ms": 45, "packet_loss": 0.2, "cpu_percent": 40, "status": "healthy"},
        {"device": "router2", "region": "nj1", "latency_ms": 130, "packet_loss": 1.8, "cpu_percent": 72, "status": "warning"},
        {"device": "switch1", "region": "nyc1", "latency_ms": 210, "packet_loss": 3.5, "cpu_percent": 88, "status": "critical"},
        {"device": "switch2", "region": "nyc2", "latency_ms": 60, "packet_loss": 0.1, "cpu_percent": 35, "status": "healthy"},
        {"device": "firewall1", "region": "dc1", "latency_ms": 175, "packet_loss": 2.2, "cpu_percent": 91, "status": "critical"},
        {"device": "ap1", "region": "phl1", "latency_ms": 95, "packet_loss": 0.7, "cpu_percent": 65, "status": "warning"}
    ]

def load_data_to_dataframe(data):
    return pd.DataFrame(data)

def find_unhealthy_devices(df):
    return df[(df["latency_ms"] > 100) | (df["packet_loss"] > 1.0) | (df["cpu_percent"] > 80)]

def summarize_devices(unhealthy_df):
    total_unhealthy = len(unhealthy_df)
    unhealthy_by_region = unhealthy_df.groupby("region")["device"].count()
    return total_unhealthy, unhealthy_by_region

def save_report(unhealthy_df):
    unhealthy_df.to_csv("network_api_report.csv", index=False)

def main():
    data = get_network_api_data()
    df = load_data_to_dataframe(data)

    unhealthy_df = find_unhealthy_devices(df)
    total_unhealthy, unhealthy_by_region = summarize_devices(unhealthy_df)

    print("=== Network Observability Summary ===")
    print(f"Total unhealthy devices: {total_unhealthy}")

    print("\nUnhealthy devices:")
    print(unhealthy_df)

    print("\nUnhealthy devices by region:")
    print(unhealthy_by_region)

    save_report(unhealthy_df)
    print("\nReport saved as network_api_report.csv")

if __name__ == "__main__":
    main()