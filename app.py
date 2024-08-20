@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    data = request.json
    if data.get('status') == 'completed':
        # Extract necessary details
        order_id = data.get('orderId')
        user_chat_id = extract_user_chat_id_from_order(order_id)
        product_details = get_product_details(order_id)
        
        # Send a message \\to the user via Telegram with pickup details
        send_telegram_message(user_chat_id, f"Your payment was successful! Here are your pickup details: {product_details}")
    
    return 'Webhook received', 200
