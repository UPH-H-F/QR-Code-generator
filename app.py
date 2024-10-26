from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import os

app = Flask(__name__)

def create_qr_with_logo(data, logo_path=None, qr_size=300, logo_size_ratio=0.2, fill_color="black", back_color="white"):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_image = qr_image.convert("RGBA")

    if logo_path:
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = int(qr_size * logo_size_ratio)
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        qr_width, qr_height = qr_image.size
        logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        qr_image.paste(logo, logo_position, logo)

    return qr_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form['url']
    logo_name = request.form.get('logo')
    fill_color = request.form.get('fill_color', 'black')  # Get fill color, default to black
    back_color = request.form.get('back_color', 'white')  # Get back color, default to white

    if logo_name:
        logo_path = os.path.join('static/images', logo_name)
        qr_image = create_qr_with_logo(data, logo_path, fill_color=fill_color, back_color=back_color)
    else:
        qr_image = create_qr_with_logo(data, fill_color=fill_color, back_color=back_color)

    qr_image_path = 'static/images/qr_with_logo.png'
    qr_image.save(qr_image_path)

    return send_file(qr_image_path)

if __name__ == '__main__':
    app.run(debug=True)