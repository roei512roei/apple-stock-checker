import os
import requests

# Pre-configured defaults for iPhone 18 Pro Max 256GB Silver near NYC 10036
PART_NUMBER = os.environ.get("PART_NUMBER", "MJW54LL/A")
ZIP_CODE = os.environ.get("ZIP_CODE", "10036")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def check_stock():
  url = f"https://www.apple.com/shop/fulfillment-messages?parts.0={PART_NUMBER}&location={ZIP_CODE}"
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"
          " AppleWebKit/605.1.15"
      )
  }

  try:
    response = requests.get(url, headers=headers).json()
    stores = response["body"]["content"]["pickupMessage"]["stores"]

    in_stock = []
    for store in stores:
      parts = store["partsAvailability"].get(PART_NUMBER, {})
      if parts.get("pickupDisplay") == "available":
        in_stock.append(store["storeName"])

    if in_stock:
      message = (
          "🚨 iPhone 18 Pro Max (Silver 256GB) IN STOCK!\nAvailable at:"
          f" {', '.join(in_stock)}"
      )
      requests.post(
          f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
          data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
      )
  except Exception as e:
    print(f"Check failed: {e}")


if __name__ == "__main__":
  check_stock()
