from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import os, json, uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-antes-de-publicar")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
DATA_FILE = os.path.join(BASE_DIR, "solicitudes.json")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024  # 15 MB por solicitud
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "webp", "doc", "docx", "xls", "xlsx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/enviar-cotizacion", methods=["POST"])
def enviar_cotizacion():
    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()
    marca = request.form.get("marca", "").strip()
    mensaje = request.form.get("mensaje", "").strip()
    archivo = request.files.get("archivo")

    if not nombre or not telefono or not marca:
        flash("Completa tu nombre, teléfono/WhatsApp y marca de interés.", "error")
        return redirect(url_for("index") + "#solicitar")

    if not archivo or not archivo.filename:
        flash("Adjunta tu documento, PDF o imagen para poder cotizar.", "error")
        return redirect(url_for("index") + "#solicitar")

    if not allowed_file(archivo.filename):
        flash("Formato no permitido. Usa PDF, imagen, Word o Excel.", "error")
        return redirect(url_for("index") + "#solicitar")

    request_id = uuid.uuid4().hex[:10].upper()
    original_name = secure_filename(archivo.filename)
    stored_name = f"{request_id}_{original_name}"
    archivo.save(os.path.join(UPLOAD_FOLDER, stored_name))

    record = {
        "id": request_id,
        "fecha": datetime.now().isoformat(timespec="minutes"),
        "nombre": nombre,
        "telefono": telefono,
        "marca": marca,
        "mensaje": mensaje,
        "archivo_original": original_name,
        "archivo_guardado": stored_name,
        "estado": "Pendiente"
    }
    records = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except (json.JSONDecodeError, OSError):
            records = []
    records.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    flash(f"¡Solicitud recibida! Tu código es {request_id}. CotizaFerre revisará el archivo y te contactará al número indicado.", "success")
    return redirect(url_for("index") + "#solicitar")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    # Ruta simple para uso local. En producción, protege esta ruta con autenticación.
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
