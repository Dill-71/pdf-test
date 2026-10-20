from flask import Flask, send_from_directory, request, send_file
import qrcode
import os
import io

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/")
def index():
    return "PDF QR Service is running."


@app.route("/download/<path:filename>")
def download_pdf(filename):
    return send_from_directory(
        UPLOAD_DIR, filename,
        as_attachment=True,
        mimetype="application/pdf"
    )


@app.route("/make_qr/<path:filename>")
def make_qr(filename):
    base = request.host_url.rstrip("/")
    download_url = f"{base}/download/{filename}"
    img = qrcode.make(download_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")