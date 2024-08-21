import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Replace with your actual OxaPay API key
OXAPAY_API_KEY = 'T7KWKH-DUKXAS-DXBMN3-ZK4RXW'
OXAPAY_API_URL = 'https://api.oxapay.com/merchants/request'

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7247878179:AAHoU-nqAoj2MR_622oBbW0T-Ha7UyuOUF0'

# Define products
PRODUCTS = {
    'product1': {'name': 'Rainbow Chip 5g', 'price': 1},  # Price in USD
    'product2': {'name': 'Product 2', 'price': 20},
}

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    keyboard = [
        [InlineKeyboardButton(PRODUCTS['product1']['name'], callback_data='product1')],
        [InlineKeyboardButton(PRODUCTS['product2']['name'], callback_data='product2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a product:', reply_markup=reply_markup)

async def product_selected(update: Update, context: CallbackContext) -> None:
    """Handles the product selection."""
    query = update.callback_query
    await query.answer()
    product_key = query.data
    product = PRODUCTS[product_key]

    # Create a payment link via OxaPay API
    payment_data = {
        'merchant': OXAPAY_API_KEY,
        'amount': product['price'],
        'currency': 'USD',
        'lifeTime': 30,  # Expiration time in minutes
        'callbackUrl': 'https://botas-ad0330beb1f6.herokuapp.com/oxapay-webhook',  # Webhook URL
      #  'returnUrl': 'https://yourdomain.com/success',  # Replace with your return URL
        'description': f'Purchase of {product["name"]}',
        'orderId': f'{update.effective_chat.id}-{product_key}',
    }

    response = requests.post(OXAPAY_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payment_data))
    payment_info = response.json()

    if response.status_code == 200 and payment_info['result'] == 100:
        payment_url = payment_info['payLink']
        await query.edit_message_text(f'Pasirinkote {product["name"]}. Kaina ${product["price"]}. Apmokekite naudodami linka: {payment_url}')
    else:
        await query.edit_message_text(f"Failed to generate payment link. Please try again later.")

def main():
    """Main function to run the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(product_selected))

    application.run_polling()

if __name__ == '__main__':
    main()
