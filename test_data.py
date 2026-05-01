from alpaca_trade_api.rest import REST
import os
from dotenv import load_dotenv

load_dotenv()

api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

bars = api.get_bars("AAPL", "5Min", limit=5).df

print("\n=== RAW DATA ===")
print(bars)

print("\n=== INFO ===")
print("Columns:", bars.columns)
print("Length:", len(bars))