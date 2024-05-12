import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_stock_price(symbol):
    """
    Fetches the current stock price from Yahoo Finance for the given symbol.
    Adjusts symbol formatting issues specific to certain stocks like 'BRK.A'.
    """
    if symbol == 'BRK.A':
        symbol = 'BRK-A'  # Adjusted symbol format for Yahoo Finance compatibility
    url = f"https://finance.yahoo.com/quote/{symbol}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_container = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        if price_container:
            return price_container.text.replace(',', '')  # Remove commas from prices like 622,000.00
        else:
            raise ValueError("Price container not found.")
    except Exception as e:
        print(f"Could not retrieve price for {symbol}. Error: {e}")
        return "N/A"

def main():
    # Load the dataset
    url = "https://raw.githubusercontent.com/gheniabla/datasets/master/fortune20_hash.csv"
    data = pd.read_csv(url, sep="#")

    # Add the 'Price' column by fetching stock prices
    data['Price'] = data['Symbol'].apply(lambda x: fetch_stock_price(x) if pd.notna(x) else "N/A")

    # Print the data
    print(data)

    # Write to CSV file
    data.to_csv("CSIT275A7_Rusak.csv", sep="#", index=False)

if __name__ == "__main__":
    main()
