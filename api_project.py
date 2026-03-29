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

def main():
    data = get_api_data()
    df = load_data_to_dataframe(data)

    print("=== API Data Preview ===")
    print(df[["id", "name", "username", "email", "city", "company_name"]].to_string())

    filtered_users = df[df["city"] == "South Christy"]
    print("\n=== Filtered Users ===")
    print(filtered_users[["name", "email", "city", "company_name"]].to_string())
  

if __name__ == "__main__":
    main()