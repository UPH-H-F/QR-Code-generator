from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form['data']
    if data:
        # Generate QR code in memory
        img = qrcode.make(data)
        byte_io = BytesIO()
        img.save(byte_io, 'PNG')
        byte_io.seek(0)
        
        # Encode the image to display on the webpage
        qr_code_data = base64.b64encode(byte_io.getvalue()).decode('utf-8')
        qrcode_image = f"data:image/png;base64,{qr_code_data}"
        
        return render_template('index.html', qrcode_image=qrcode_image)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
