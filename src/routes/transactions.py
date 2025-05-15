from flask import Blueprint, render_template
import datetime
import pytz

transactions_bp = Blueprint('transactions', __name__, template_folder='../templates')

def format_timestamp_to_beijing(timestamp_ms):
    """Converts a UNIX timestamp (in milliseconds) to a Beijing time string."""
    if timestamp_ms is None:
        return "N/A"
    try:
        # Convert milliseconds to seconds
        timestamp_s = timestamp_ms / 1000.0
        utc_dt = datetime.datetime.fromtimestamp(timestamp_s, tz=datetime.timezone.utc)
        beijing_tz = pytz.timezone('Asia/Shanghai')
        beijing_dt = utc_dt.astimezone(beijing_tz)
        return beijing_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return "Invalid Date"

# Mock data simulating API response from app-store-server-library-python
# Based on Get Transaction History: https://developer.apple.com/documentation/appstoreserverapi/get_transaction_history
# And TransactionInfo: https://developer.apple.com/documentation/appstoreserverapi/transactioninfo
mock_transactions_data = [
    {
        "transactionId": "1000000123456789",
        "originalTransactionId": "1000000123456789",
        "bundleId": "com.example.myapp",
        "productId": "com.example.product.tier1",
        "purchaseDate": 1678886400000,  # March 15, 2023 12:00:00 PM UTC
        "originalPurchaseDate": 1678886400000,
        "quantity": 1,
        "type": "Auto-Renewable Subscription", # Could be 'Non-Consumable', 'Consumable', 'Non-Renewing Subscription'
        "inAppOwnershipType": "PURCHASED",
        "signedDate": 1678886460000,
        "environment": "Production",
        "storefront": "USA",
        "price": 999, # in cents or local currency unit * 1000
        "currency": "USD"
    },
    {
        "transactionId": "1000000123456790",
        "originalTransactionId": "1000000123456790",
        "bundleId": "com.example.myapp",
        "productId": "com.example.product.monthly",
        "purchaseDate": 1681560000000,  # April 15, 2023 12:00:00 PM UTC
        "originalPurchaseDate": 1681560000000,
        "quantity": 1,
        "type": "Auto-Renewable Subscription",
        "inAppOwnershipType": "PURCHASED",
        "signedDate": 1681560060000,
        "environment": "Production",
        "storefront": "CHN",
        "price": 6800, # 68.00 CNY
        "currency": "CNY"
    },
    {
        "transactionId": "1000000123456791",
        "originalTransactionId": "1000000123456791",
        "bundleId": "com.example.myapp",
        "productId": "com.example.feature.unlock",
        "purchaseDate": 1684152000000,  # May 15, 2023 12:00:00 PM UTC
        "originalPurchaseDate": 1684152000000,
        "quantity": 1,
        "type": "Non-Consumable",
        "inAppOwnershipType": "PURCHASED",
        "signedDate": 1684152060000,
        "environment": "Production",
        "storefront": "GBR",
        "price": 499, # 4.99 GBP
        "currency": "GBP"
    }
]

@transactions_bp.route('/history')
def history():
    formatted_transactions = []
    for t in mock_transactions_data:
        formatted_t = t.copy()
        formatted_t['purchaseDateFormatted'] = format_timestamp_to_beijing(t.get('purchaseDate'))
        formatted_t['originalPurchaseDateFormatted'] = format_timestamp_to_beijing(t.get('originalPurchaseDate'))
        formatted_t['signedDateFormatted'] = format_timestamp_to_beijing(t.get('signedDate'))
        # Format price (assuming price is in smallest currency unit, e.g., cents)
        formatted_t['priceFormatted'] = f"{t.get('price', 0) / 100.0:.2f} {t.get('currency', '')}" if t.get('price') is not None and t.get('currency') else "N/A"
        formatted_transactions.append(formatted_t)
    return render_template('transactions.html', transactions=formatted_transactions)

