from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Render!"

@app.route('/oxapay-webhook', methods=['POST'])
def oxapay_webhook():
    data = request.json
    print("Webhook received:", data)
    return 'Webhook received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
