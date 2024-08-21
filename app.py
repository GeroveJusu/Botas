from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your actual OxaPay API key and Telegram bot token
OXAPAY_API_KEY = 'T7KWKH-DUKXAS-DXBMN3-ZK4RXW'
TELEGRAM_BOT_TOKEN = '7247878179:AAHoU-nqAoj2MR_622oBbW0T-Ha7UyuOUF0'

# Define products
PRODUCTS = {
    'product1': {'name': 'Rainbow Chip 5g', 'price': 80},
    'product2': {'name': 'Product 2', 'price': 20},
}

# Example product locations for pickup
PRODUCT_LOCATIONS = {
    'product1': [{'id': 1, 'location': 'Location 1'}, {'id': 2, 'location': 'Location 2'}],
    'product2': [{'id': 1, 'location': 'Location A'}, {'id': 2, 'location': 'Location B'}],
}

def send_telegram_message(chat_id, text):
    """Send a message via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    print(f"Sending message to {chat_id}: {text}")
    print(f"Telegram response: {response.text}")

def get_available_location(product_key):
    """Get an available pickup location for a product."""
    locations = PRODUCT_LOCATIONS.get(product_key, [])
    if locations:
        return locations.pop(0)  # Remove and return the first available location
    return None

def remove_location(product_key, location_id):
    """Remove a location from the product's location list after it's been used."""
    PRODUCT_LOCATIONS[product_key] = [
        loc for loc in PRODUCT_LOCATIONS[product_key] if loc['id'] != location_id
    ]

@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    """Handle the incoming webhook from OxaPay."""
    data = request.json
    print("Webhook received:", data)  # Debugging statement

    if data.get('status') == 'Paid':
        order_id = data.get('orderId')
        chat_id, product_key = order_id.split('-')
        product = PRODUCTS.get(product_key)

        if product:
            location = get_available_location(product_key)
            if location:
                # Send pickup details to the user
                pickup_details = f"Your payment for {product['name']} was successful. You can pick up your product at {location['location']}."
                send_telegram_message(chat_id, pickup_details)
                remove_location(product_key, location['id'])
            else:
                send_telegram_message(chat_id, "Sorry, this product is currently out of stock.")
        else:
            send_telegram_message(chat_id, "Product not found.")
    else:
        print(f"Received status: {data.get('status')} - no action taken.")

    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
