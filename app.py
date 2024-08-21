from flask import Flask, request
import requests

app = Flask(__name__)

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7247878179:AAHoU-nqAoj2MR_622oBbW0T-Ha7UyuOUF0'

# Product details with available stock and pickup locations
PRODUCTS = {
    'product1': {
        'name': 'Rainbow Chip 5g',
        'stock': [
            {'location': '123 Main St', 'id': 'loc1'},
            {'location': '456 Oak St', 'id': 'loc2'},
            {'location': '789 Pine St', 'id': 'loc3'},
        ]
    },
    'product2': {
        'name': 'Product 2',
        'stock': [
            {'location': '987 Elm St', 'id': 'loc1'},
            {'location': '654 Maple St', 'id': 'loc2'},
        ]
    },
}

# Function to get the first available pickup location for a product
def get_available_location(product_key):
    product = PRODUCTS.get(product_key)
    if product and product['stock']:
        return product['stock'][0]  # Return the first available location
    return None

# Function to remove a location from stock after a successful payment
def remove_location(product_key, location_id):
    product = PRODUCTS.get(product_key)
    if product:
        product['stock'] = [loc for loc in product['stock'] if loc['id'] != location_id]

@app.route('/')
def index():
    return "Hello, Heroku!"

@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    data = request.json
    print("Webhook received:", data)

    if data.get('status') == 'completed':
        order_id = data.get('orderId')
        chat_id, product_key = order_id.split('-')
        product = PRODUCTS.get(product_key)

        if product:
            location = get_available_location(product_key)
            if location:
                # Send pickup details to the user
                pickup_details = f"Your payment for {product['name']} was successful. You can pick up your product at {location['location']}."
                send_telegram_message(chat_id, pickup_details)
                
                # Remove the used location from the stock
                remove_location(product_key, location['id'])
            else:
                # Handle the case where no locations are available
                send_telegram_message(chat_id, "Sorry, this product is currently out of stock.")
    
    return 'Webhook received', 200

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
