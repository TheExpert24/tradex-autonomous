from data.alpaca_data import DataClient

def main():
    data = DataClient()

    df = data.get_bars("AAPL")

    print(df.tail())
    print("Rows:", len(df))

if __name__ == "__main__":
    main()