from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import requests
import os
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/generated_images/'

class Generate:
    def __init__(self):
        self.TOKEN = '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'
        self.API_URL = None
        self.headers = {"Authorization": f"Bearer {self.TOKEN}"}

    def generate(self, input_text):
        payload = {"inputs": input_text}
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return io.BytesIO(response.content)

    def choice(self, choice):
        if choice == 0:
            self.API_URL = "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.0"
        elif choice == 1:
            self.API_URL = "https://api-inference.huggingface.co/models/nerijs/pixel-art-xl"
        elif choice == 2:
            self.API_URL = "https://api-inference.huggingface.co/models/iamkaikai/CUBISM-LORA"
        elif choice == 3:
            self.API_URL = "https://api-inference.huggingface.co/models/stablediffusionapi/disney-pixar-cartoon"
        elif choice == 4:
            self.API_URL = "https://api-inference.huggingface.co/models/blink7630/storyboard-sketch"

gen = Generate()

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_image_path = None

    if request.method == 'POST':
        text = request.form['text']
        style_choice = int(request.form['style'])

        # Set the API URL based on the user's style choice
        gen.choice(style_choice)

        # Generate an image based on the input text and style choice
        image_bytes = gen.generate(text)

        # Save the generated image
        generated_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_image.jpg')
        with open(generated_image_path, 'wb') as img_file:
            img_file.write(image_bytes.read())

    return render_template('index.html', generated_image_path=generated_image_path)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)
