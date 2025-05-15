from flask import Blueprint, render_template
import datetime
import pytz

subscriptions_bp = Blueprint("subscriptions", __name__, template_folder="../templates")

def format_timestamp_to_beijing(timestamp_ms):
    """Converts a UNIX timestamp (in milliseconds) to a Beijing time string."""
    if timestamp_ms is None:
        return "N/A"
    try:
        timestamp_s = timestamp_ms / 1000.0
        utc_dt = datetime.datetime.fromtimestamp(timestamp_s, tz=datetime.timezone.utc)
        beijing_tz = pytz.timezone("Asia/Shanghai")
        beijing_dt = utc_dt.astimezone(beijing_tz)
        return beijing_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return "Invalid Date"

# Mock data simulating API response from app-store-server-library-python
# Based on Get All Subscription Statuses: https://developer.apple.com/documentation/appstoreserverapi/getallsubscriptionstatuses
# And SubscriptionGroupIdentifierItem, LastTransactionsItem, JWSRenewalInfo, JWSTransaction
mock_subscriptions_data = [
    {
        "subscriptionGroupIdentifier": "sub_group_A",
        "lastTransactions": [
            {
                "originalTransactionId": "2000000123456789",
                "status": 1,  # 1: Active, 2: Expired, 3: In Billing Retry, 4: In Grace Period, 5: Revoked
                "signedRenewalInfo": {
                    "autoRenewProductId": "com.example.product.monthly.A",
                    "autoRenewStatus": 1, # 1: Will renew, 0: Turned off
                    "expirationIntent": 1, # 1: Customer canceled, 2: Billing error, etc.
                    "gracePeriodExpiresDate": 1690000000000, # Example: July 22, 2023
                    "isInBillingRetryPeriod": False,
                    "offerIdentifier": "OFFER_CODE_XYZ",
                    "offerType": 1, # 1: Intro, 2: Promo, 3: Subscription Offer
                    "originalTransactionId": "2000000123456789",
                    "priceIncreaseStatus": 0, # 0: No increase, 1: Pending
                    "productId": "com.example.product.monthly.A",
                    "signedDate": 1688169600000 # July 1, 2023
                },
                "signedTransactionInfo": {
                    "appAccountToken": "user-guid-123",
                    "bundleId": "com.example.myapp",
                    "currency": "USD",
                    "environment": "Production",
                    "expiresDate": 1690847999000, # July 31, 2023 23:59:59 UTC
                    "inAppOwnershipType": "PURCHASED",
                    "originalPurchaseDate": 1680307200000, # April 1, 2023
                    "originalTransactionId": "2000000123456789",
                    "price": 999,
                    "productId": "com.example.product.monthly.A",
                    "purchaseDate": 1688169600000, # July 1, 2023
                    "quantity": 1,
                    "revocationDate": None,
                    "revocationReason": None,
                    "signedDate": 1688169660000,
                    "subscriptionGroupIdentifier": "sub_group_A",
                    "transactionId": "2000000987654321",
                    "type": "Auto-Renewable Subscription",
                    "webOrderLineItemId": "web_order_1"
                }
            }
        ]
    },
    {
        "subscriptionGroupIdentifier": "sub_group_B",
        "lastTransactions": [
            {
                "originalTransactionId": "3000000123456789",
                "status": 2,
                "signedRenewalInfo": {
                    "autoRenewProductId": "com.example.product.yearly.B",
                    "autoRenewStatus": 0,
                    "expirationIntent": 1,
                    "gracePeriodExpiresDate": None,
                    "isInBillingRetryPeriod": False,
                    "offerIdentifier": None,
                    "offerType": None,
                    "originalTransactionId": "3000000123456789",
                    "priceIncreaseStatus": 0,
                    "productId": "com.example.product.yearly.B",
                    "signedDate": 1672531200000 # Jan 1, 2023
                },
                "signedTransactionInfo": {
                    "appAccountToken": "user-guid-456",
                    "bundleId": "com.example.anotherapp",
                    "currency": "EUR",
                    "environment": "Production",
                    "expiresDate": 1704067199000, # Dec 31, 2023 23:59:59 UTC
                    "inAppOwnershipType": "PURCHASED",
                    "originalPurchaseDate": 1672531200000, # Jan 1, 2023
                    "originalTransactionId": "3000000123456789",
                    "price": 4999,
                    "productId": "com.example.product.yearly.B",
                    "purchaseDate": 1672531200000, # Jan 1, 2023
                    "quantity": 1,
                    "revocationDate": None,
                    "revocationReason": None,
                    "signedDate": 1672531260000,
                    "subscriptionGroupIdentifier": "sub_group_B",
                    "transactionId": "3000000987654321",
                    "type": "Auto-Renewable Subscription",
                    "webOrderLineItemId": "web_order_2"
                }
            }
        ]
    }
]

def get_status_description(status_code):
    status_map = {
        1: "Active",
        2: "Expired",
        3: "In Billing Retry",
        4: "In Grace Period",
        5: "Revoked"
    }
    return status_map.get(status_code, "Unknown")

def get_autorenew_status_description(status_code):
    return "Will Renew" if status_code == 1 else "Turned Off"

@subscriptions_bp.route("/status")
def status_all():
    processed_subscriptions = []
    for sub_group in mock_subscriptions_data:
        processed_group = {"subscriptionGroupIdentifier": sub_group["subscriptionGroupIdentifier"], "transactions": []}
        for lt in sub_group.get("lastTransactions", []):
            processed_lt = lt.copy()
            # Format dates in signedRenewalInfo
            if "signedRenewalInfo" in processed_lt and processed_lt["signedRenewalInfo"]:
                sri = processed_lt["signedRenewalInfo"]
                sri["gracePeriodExpiresDateFormatted"] = format_timestamp_to_beijing(sri.get("gracePeriodExpiresDate"))
                sri["signedDateFormatted"] = format_timestamp_to_beijing(sri.get("signedDate"))
                sri["autoRenewStatusFormatted"] = get_autorenew_status_description(sri.get("autoRenewStatus"))

            # Format dates and other fields in signedTransactionInfo
            if "signedTransactionInfo" in processed_lt and processed_lt["signedTransactionInfo"]:
                sti = processed_lt["signedTransactionInfo"]
                sti["expiresDateFormatted"] = format_timestamp_to_beijing(sti.get("expiresDate"))
                sti["originalPurchaseDateFormatted"] = format_timestamp_to_beijing(sti.get("originalPurchaseDate"))
                sti["purchaseDateFormatted"] = format_timestamp_to_beijing(sti.get("purchaseDate"))
                sti["revocationDateFormatted"] = format_timestamp_to_beijing(sti.get("revocationDate"))
                sti["signedDateFormatted"] = format_timestamp_to_beijing(sti.get("signedDate"))
                sti["priceFormatted"] = f"{sti.get('price', 0) / 100.0:.2f} {sti.get('currency', '')}" if sti.get('price') is not None and sti.get('currency') else "N/A"

            processed_lt["statusFormatted"] = get_status_description(lt.get("status"))
            processed_group["transactions"].append(processed_lt)
        processed_subscriptions.append(processed_group)
    return render_template("subscriptions.html", subscriptions=processed_subscriptions)

