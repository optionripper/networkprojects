import pandas as pd
from datetime import datetime

LATENCY_THRESHOLD = 100
PACKET_LOSS_THRESHOLD = 1.0
CPU_THRESHOLD = 80

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
    return df[
        (df["latency_ms"] > LATENCY_THRESHOLD) |
        (df["packet_loss"] > PACKET_LOSS_THRESHOLD) |
        (df["cpu_percent"] > CPU_THRESHOLD)
    ].copy()

def add_issue_reason(unhealthy_df):
    def get_reason(row):
        reasons = []

        if row["latency_ms"] > LATENCY_THRESHOLD:
            reasons.append("high latency")
        if row["packet_loss"] > PACKET_LOSS_THRESHOLD:
            reasons.append("packet loss")
        if row["cpu_percent"] > CPU_THRESHOLD:
            reasons.append("high cpu")

        return ", ".join(reasons)

    unhealthy_df["issue_reason"] = unhealthy_df.apply(get_reason, axis=1)
    return unhealthy_df

def save_report(unhealthy_df):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"network_api_report_{timestamp}.csv"
    unhealthy_df.to_csv(filename, index=False)
    print(f"\nReport saved as {filename}")

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
    unhealthy_df = add_issue_reason(unhealthy_df)

    unhealthy_df_sorted = unhealthy_df.sort_values(
        by=["packet_loss", "latency_ms", "cpu_percent"],
        ascending=False
    )

    total_unhealthy, unhealthy_by_region = summarize_devices(unhealthy_df)

    print("=== Network Observability Summary ===")
    print(f"Total unhealthy devices: {total_unhealthy}")

    print("\nTop issues:")
    print(unhealthy_df_sorted[["device", "region", "latency_ms", "packet_loss", "cpu_percent", "issue_reason"]].to_string())

    save_report(unhealthy_df_sorted)
    print("\nReport saved as network_api_report.csv")

if __name__ == "__main__":
    main()