from flask import Blueprint, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

prodigi_bp = Blueprint('prodigi', __name__)

PRODIGI_API_KEY = os.getenv("PRODIGI_API_KEY")
PRODIGI_BASE_URL = "https://api.sandbox.prodigi.com/v4.0"  # Use prod URL for production

HEADERS = {
    "X-API-Key": PRODIGI_API_KEY,
    "Content-Type": "application/json"
}

# --- Interface-style order validation (lightweight) ---
def validate_order(order):
    required_fields = ["merchantReference", "recipient", "items"]
    for field in required_fields:
        if field not in order:
            return False, f"Missing required field: {field}"

    recipient = order["recipient"]
    if not recipient.get("name") or not recipient.get("address"):
        return False, "Recipient name and address are required"

    if not isinstance(order["items"], list) or not order["items"]:
        return False, "At least one item is required"

    return True, "Valid"

# --- POST /prodigi/order ---
@prodigi_bp.route("/prodigi/orders", methods=["POST"])
def create_order():
    order = {
        "merchantReference": "MyMerchantReference1",
        "shippingMethod": "Overnight",
        "recipient": {
            "name": "Mr Testy McTestface",
            "address": {
                "line1": "14 test place",
                "line2": "test",
                "postalOrZipCode": "12345",
                "countryCode": "US",
                "townOrCity": "somewhere",
                "stateOrCounty": "null"
            }
        },
        "items": [
            {
                "merchantReference": "item #1",
                "sku": "GLOBAL-CFPM-16X20",
                "copies": 1,
                "sizing": "fillPrintArea",
                "attributes": {
                    "color": "black"
                },
                "assets": [
                    {
                        "printArea": "default",
                        "url": "https://pwintyimages.blob.core.windows.net/samples/stars/test-sample-grey.png",
                        "md5Hash": "daa1c811c6038e718a23f0d816914b7b",
                        "pageCount": 50
                    }
                ]
            }
        ],
        "metadata": {
            "mycustomkey":"some-guid",
            "someCustomerPreference": {
                "preference1": "something",
                "preference2": "red"
            },
            "sourceId": 12345
        }
    }
    try:
        response = requests.post(
            f"{PRODIGI_BASE_URL}/orders",
            headers=HEADERS,
            json=order
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error creating order: {response}")
        return jsonify({"error": str(e)}), 500

# --- POST /prodigi/quote ---
@prodigi_bp.route("/prodigi/quote", methods=["POST"])
def get_quote():
    #order = request.get_json()
    order = {
        "shippingMethod": "standard",
        "destinationCountryCode": "US",
        "currencyCode":"USD",
        "items": [
            {
                "sku": "GLOBAL-TATT-S",
                "copies": 5,
                "assets" : [
                    { "printArea" : "default" }
                ]
            }
        ]
    }
    print(f"Fetching quote for order: {order}")
    try:
        response = requests.post(
            f"{PRODIGI_BASE_URL}/quotes",
            headers=HEADERS,
            json=order
        )
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- GET /prodigi/product/<sku> ---
@prodigi_bp.route("/prodigi/product/<sku>", methods=["GET"])
def get_product_details(sku):
    print(f"Fetching product details for SKU: {sku}")
    try:
        response = requests.get(
            f"{PRODIGI_BASE_URL}/products/{sku}",
            headers=HEADERS
        )
        print(f"Headers: {HEADERS}")
        print(f"Fetching product details for SKU: {sku}")
        print(f"Response: {response}")
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
