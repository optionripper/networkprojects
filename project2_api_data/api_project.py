import requests
import pandas as pd

def get_api_data():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    return response.json()

def load_data_to_dataframe(data):
    df = pd.DataFrame(data)
    df["city"] = df["address"].apply(lambda x: x["city"])
    df["company_name"] = df["company"].apply(lambda x: x["name"])
    return df

def find_target_records(df):
    return df[df["city"] == "South Christy"]

def summarize_records(filtered_df):
    total_records = len(filtered_df)
    records_by_company = filtered_df.groupby("company_name")["id"].count()
    return total_records, records_by_company

def save_report(filtered_df):
    filtered_df.to_csv("api_filtered_report.csv", index=False)

def main():
    data = get_api_data()
    df = load_data_to_dataframe(data)

    filtered_df = find_target_records(df)
    total_records, records_by_company = summarize_records(filtered_df)

    print("=== API Data Summary ===")
    print(f"Total filtered records: {total_records}")

    print("\nFiltered rows:")
    print(filtered_df[["id", "name", "email", "city", "company_name"]])

    print("\nRecords by company:")
    print(records_by_company)

    save_report(filtered_df)
    print("\nReport saved as api_filtered_report.csv")

if __name__ == "__main__":
    main()